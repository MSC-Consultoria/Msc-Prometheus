"""Utility for loading normalized match data into Supabase tables.

The loader expects a dictionary with the following optional keys:
- "players": list of player records (must include ``player_id``)
- "matches": list of match records (must include ``match_id``)
- "heroes": list of hero metadata rows (``hero_id`` required)
- "items": list of item metadata rows (``item_id`` required)
- "player_matches": list of player-match stat rows (composite key ``match_id`` + ``player_id``)
- "interval_stats": list of interval stat rows (composite key ``match_id`` + ``player_id`` + ``interval_start_seconds``)

Upserts use the identifying keys above so repeated runs remain idempotent. After
loading, the loader performs basic integrity checks: row counts relative to the
payload and foreign-key presence for players, matches, and heroes referenced in
``player_matches`` and ``interval_stats``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Sequence

import httpx
from dotenv import load_dotenv
from supabase import Client, ClientOptions, PostgrestClientOptions, create_client

load_dotenv()

NormalizedPayload = Mapping[str, Sequence[MutableMapping[str, Any]]]


@dataclass
class SupabaseSettings:
    """Environment-driven Supabase configuration."""

    url: str
    key: str
    pool_size: int = 10
    schema: str = "public"

    @classmethod
    def from_env(cls) -> "SupabaseSettings":
        """Load settings from environment variables.

        Required variables:
        - ``SUPABASE_URL``
        - ``SUPABASE_SERVICE_ROLE_KEY`` or ``SUPABASE_KEY``
        Optional:
        - ``SUPABASE_POOL_SIZE`` to cap HTTP connection pooling (default: 10)
        - ``SUPABASE_SCHEMA`` to override the target schema (default: public)
        """

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_KEY) are required")

        pool_size = int(os.getenv("SUPABASE_POOL_SIZE", "10"))
        schema = os.getenv("SUPABASE_SCHEMA", "public")
        return cls(url=url, key=key, pool_size=pool_size, schema=schema)


class SupabaseLoader:
    """Supabase data loader with idempotent upserts and integrity checks."""

    def __init__(self, settings: SupabaseSettings):
        http_client = httpx.Client(
            limits=httpx.Limits(max_connections=settings.pool_size, max_keepalive_connections=settings.pool_size),
            timeout=httpx.Timeout(30.0),
        )
        options = ClientOptions(postgrest_client_options=PostgrestClientOptions(schema=settings.schema), http_client=http_client)
        self.client: Client = create_client(settings.url, settings.key, options)

    def load_payload(self, payload: NormalizedPayload) -> Dict[str, Any]:
        """Upsert all supported entities and validate the resulting dataset."""

        upserted = {
            "players": self._upsert_table("players", payload.get("players", []), ["player_id"]),
            "matches": self._upsert_table("matches", payload.get("matches", []), ["match_id"]),
            "heroes": self._upsert_table("heroes", payload.get("heroes", []), ["hero_id"]),
            "items": self._upsert_table("items", payload.get("items", []), ["item_id"]),
            "player_matches": self._upsert_table("player_matches", payload.get("player_matches", []), ["match_id", "player_id"]),
            "interval_stats": self._upsert_table(
                "interval_stats",
                payload.get("interval_stats", []),
                ["match_id", "player_id", "interval_start_seconds"],
            ),
        }

        integrity = self._run_integrity_checks(payload)
        return {"upserted": upserted, "integrity": integrity}

    def _upsert_table(self, table: str, rows: Sequence[MutableMapping[str, Any]], conflict_keys: Sequence[str]) -> int:
        if not rows:
            return 0

        response = self.client.table(table).upsert(rows, on_conflict=",".join(conflict_keys)).execute()
        return len(response.data or [])

    def _run_integrity_checks(self, payload: NormalizedPayload) -> Dict[str, Any]:
        checks: Dict[str, Any] = {
            "row_counts": {},
            "foreign_keys": {},
        }

        expected_counts = {
            "players": len(payload.get("players", [])),
            "matches": len(payload.get("matches", [])),
            "heroes": len(payload.get("heroes", [])),
            "items": len(payload.get("items", [])),
            "player_matches": len(payload.get("player_matches", [])),
            "interval_stats": len(payload.get("interval_stats", [])),
        }

        for table, expected in expected_counts.items():
            actual = self._count_rows(table)
            checks["row_counts"][table] = {
                "expected_at_least": expected,
                "actual": actual,
                "ok": actual >= expected,
            }

        player_ids = {row.get("player_id") for row in payload.get("player_matches", []) if row.get("player_id")}
        player_ids.update({row.get("player_id") for row in payload.get("interval_stats", []) if row.get("player_id")})
        match_ids = {row.get("match_id") for row in payload.get("player_matches", []) if row.get("match_id")}
        match_ids.update({row.get("match_id") for row in payload.get("interval_stats", []) if row.get("match_id")})
        hero_ids = {row.get("hero_id") for row in payload.get("player_matches", []) if row.get("hero_id")}

        checks["foreign_keys"]["players"] = self._check_ids_exist("players", "player_id", player_ids)
        checks["foreign_keys"]["matches"] = self._check_ids_exist("matches", "match_id", match_ids)
        checks["foreign_keys"]["heroes"] = self._check_ids_exist("heroes", "hero_id", hero_ids)

        return checks

    def _count_rows(self, table: str) -> int:
        response = self.client.table(table).select("*", count="exact").range(0, 0).execute()
        if response.count is not None:
            return response.count
        return len(response.data or [])

    def _check_ids_exist(self, table: str, column: str, values: Iterable[Any]) -> Dict[str, Any]:
        identifiers = [value for value in values if value is not None]
        if not identifiers:
            return {"checked": 0, "matched": 0, "ok": True}

        matched = 0
        for chunk in _chunked(identifiers, 500):
            response = self.client.table(table).select(column, count="exact").in_(column, chunk).execute()
            matched += response.count or len(response.data or [])

        return {"checked": len(identifiers), "matched": matched, "ok": matched == len(identifiers)}


def _chunked(items: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


if __name__ == "__main__":
    import json
    from pathlib import Path

    settings = SupabaseSettings.from_env()
    loader = SupabaseLoader(settings)

    sample_path = Path(os.getenv("DATA_PAYLOAD", ""))
    if sample_path.is_file():
        payload = json.loads(sample_path.read_text(encoding="utf-8"))
    else:
        payload = {"players": [], "matches": [], "heroes": [], "items": [], "player_matches": [], "interval_stats": []}

    result = loader.load_payload(payload)
    print(json.dumps(result, indent=2))
