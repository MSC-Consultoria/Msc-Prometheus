"""Supabase loader for normalized match analytics data.

This loader expects a normalized payload with the following collections:
- players
- matches
- heroes
- items
- player_matches
- interval_stats

It upserts data into Supabase using primary/conflict keys, refreshes materialized
views, and performs basic integrity checks after the load.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

import httpx
from supabase import Client, create_client
from supabase.lib.client_options import ClientOptions


@dataclass
class SupabaseConfig:
    """Configuration sourced from environment variables."""

    url: str
    key: str
    schema: str = "public"
    pool_size: int = 10
    timeout_seconds: float = 30.0

    @classmethod
    def from_env(cls) -> "SupabaseConfig":
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise EnvironmentError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY) must be set")

        pool_size = int(os.getenv("SUPABASE_HTTP_POOL_SIZE", "10"))
        timeout_seconds = float(os.getenv("SUPABASE_TIMEOUT_SECONDS", "30"))
        schema = os.getenv("SUPABASE_SCHEMA", "public")
        return cls(url=url, key=key, schema=schema, pool_size=pool_size, timeout_seconds=timeout_seconds)

    def http_client(self) -> httpx.Client:
        return httpx.Client(
            timeout=self.timeout_seconds,
            limits=httpx.Limits(
                max_connections=self.pool_size,
                max_keepalive_connections=self.pool_size,
            ),
        )


class SupabaseLoader:
    def __init__(self, config: SupabaseConfig):
        self.config = config
        client_options = ClientOptions(schema=config.schema, auto_refresh_token=False, persist_session=False, http_client=config.http_client())
        self.client: Client = create_client(config.url, config.key, options=client_options)

    def upsert_table(self, table: str, rows: Sequence[Dict[str, Any]], conflict_keys: Sequence[str]) -> int:
        if not rows:
            return 0
        response = self.client.table(table).upsert(rows, on_conflict=",".join(conflict_keys), count="exact").execute()
        return int(response.count or 0)

    def refresh_materialized_views(self) -> None:
        rpc_names = [
            "refresh_materialized_view_mv_player_kda_period",
            "refresh_materialized_view_mv_hero_win_rates",
            "refresh_materialized_view_mv_item_timings",
        ]
        for rpc in rpc_names:
            try:
                self.client.rpc(rpc).execute()
            except Exception:
                # If RPC helpers are not present, silently continue. Direct SQL access is unavailable via supabase-py.
                continue

    def load_payload(self, payload: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
        """Load a normalized payload into Supabase with ordered upserts."""

        self._validate_foreign_key_inputs(payload)

        counts = {
            "heroes": self.upsert_table("heroes", payload.get("heroes", []), ["hero_id"]),
            "items": self.upsert_table("items", payload.get("items", []), ["item_id"]),
            "players": self.upsert_table("players", payload.get("players", []), ["player_id"]),
            "matches": self.upsert_table("matches", payload.get("matches", []), ["match_id"]),
            "player_matches": self.upsert_table("player_matches", payload.get("player_matches", []), ["player_id", "match_id"]),
            "interval_stats": self.upsert_table(
                "interval_stats",
                payload.get("interval_stats", []),
                ["match_id", "player_id", "metric", "interval_start_seconds", "interval_end_seconds"],
            ),
        }

        self.refresh_materialized_views()
        counts.update(self.validate_row_counts(payload))
        counts.update(self.validate_foreign_keys_after_load())
        return counts

    def validate_row_counts(self, payload: Dict[str, List[Dict[str, Any]]]) -> Dict[str, int]:
        """Compare expected row counts with remote table counts."""

        results: Dict[str, int] = {}
        for table_name, rows in payload.items():
            try:
                response = self.client.table(table_name).select("*", count="exact").limit(1).execute()
                remote_count = int(response.count or 0)
            except Exception:
                remote_count = -1
            results[f"{table_name}_remote_count"] = remote_count
            results[f"{table_name}_expected_count"] = len(rows)
        return results

    def validate_foreign_keys_after_load(self) -> Dict[str, int]:
        """Check for missing player/match references after inserts."""

        players_resp = self.client.table("players").select("player_id").execute()
        matches_resp = self.client.table("matches").select("match_id").execute()
        player_ids = {row["player_id"] for row in players_resp.data or []}
        match_ids = {row["match_id"] for row in matches_resp.data or []}

        player_matches_resp = self.client.table("player_matches").select("player_id,match_id").execute()
        interval_resp = self.client.table("interval_stats").select("player_id,match_id").execute()

        missing_player_refs = len([row for row in (player_matches_resp.data or []) if row["player_id"] not in player_ids])
        missing_match_refs = len([row for row in (player_matches_resp.data or []) if row["match_id"] not in match_ids])
        missing_interval_player_refs = len([row for row in (interval_resp.data or []) if row["player_id"] not in player_ids])
        missing_interval_match_refs = len([row for row in (interval_resp.data or []) if row["match_id"] not in match_ids])

        return {
            "player_matches_missing_players": missing_player_refs,
            "player_matches_missing_matches": missing_match_refs,
            "interval_stats_missing_players": missing_interval_player_refs,
            "interval_stats_missing_matches": missing_interval_match_refs,
        }

    def _validate_foreign_key_inputs(self, payload: Dict[str, List[Dict[str, Any]]]) -> None:
        players = {row.get("player_id") for row in payload.get("players", [])}
        matches = {row.get("match_id") for row in payload.get("matches", [])}

        missing_players = [row for row in payload.get("player_matches", []) if row.get("player_id") not in players]
        missing_matches = [row for row in payload.get("player_matches", []) if row.get("match_id") not in matches]
        missing_interval_players = [row for row in payload.get("interval_stats", []) if row.get("player_id") not in players]
        missing_interval_matches = [row for row in payload.get("interval_stats", []) if row.get("match_id") not in matches]

        if missing_players or missing_matches or missing_interval_players or missing_interval_matches:
            raise ValueError(
                "Payload references missing entities: "
                f"player_matches missing players={len(missing_players)}, "
                f"player_matches missing matches={len(missing_matches)}, "
                f"interval_stats missing players={len(missing_interval_players)}, "
                f"interval_stats missing matches={len(missing_interval_matches)}"
            )


def load_from_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_loader(payload_path: Optional[str] = None) -> Dict[str, int]:
    config = SupabaseConfig.from_env()
    loader = SupabaseLoader(config)
    payload = load_from_file(payload_path) if payload_path else {
        "players": [],
        "matches": [],
        "heroes": [],
        "items": [],
        "player_matches": [],
        "interval_stats": [],
    }
    return loader.load_payload(payload)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Load normalized analytics data into Supabase.")
    parser.add_argument("--payload", help="Path to a JSON file containing normalized data.")
    args = parser.parse_args()
    results = run_loader(args.payload)
    print(json.dumps(results, indent=2))
