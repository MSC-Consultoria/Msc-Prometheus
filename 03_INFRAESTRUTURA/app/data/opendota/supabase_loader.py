"""Supabase schema + loader for OpenDota tournament analytics."""

from __future__ import annotations

import json
import os
from typing import Dict, Iterable, List, Optional

import psycopg2
from supabase import Client, create_client

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS public.players (
    account_id bigint PRIMARY KEY,
    personaname text,
    name text,
    avatarfull text,
    last_login timestamptz,
    rank_tier integer,
    leaderboard_rank integer,
    mmr_estimate integer,
    tracked_until timestamptz
);

CREATE TABLE IF NOT EXISTS public.matches (
    match_id bigint PRIMARY KEY,
    duration integer,
    start_time integer,
    radiant_win boolean,
    radiant_score integer,
    dire_score integer,
    tower_status_radiant integer,
    tower_status_dire integer,
    leagueid integer,
    cluster integer,
    game_mode integer,
    engine integer
);

CREATE TABLE IF NOT EXISTS public.player_matches (
    account_id bigint REFERENCES public.players(account_id),
    match_id bigint REFERENCES public.matches(match_id),
    player_slot integer,
    hero_id integer,
    kills integer,
    deaths integer,
    assists integer,
    gold_per_min integer,
    xp_per_min integer,
    last_hits integer,
    denies integer,
    hero_damage integer,
    tower_damage integer,
    hero_healing integer,
    duration integer,
    start_time integer,
    lane integer,
    lane_role integer,
    is_roaming boolean,
    is_radiant boolean,
    win integer,
    leaver_status integer,
    party_size integer,
    item_0 integer,
    item_1 integer,
    item_2 integer,
    item_3 integer,
    item_4 integer,
    item_5 integer,
    backpack_0 integer,
    backpack_1 integer,
    backpack_2 integer,
    PRIMARY KEY (account_id, match_id)
);
"""


class SupabaseSchemaManager:
    """Applies the OpenDota schema using a Postgres connection string."""

    def __init__(self, connection_uri: Optional[str] = None) -> None:
        self.connection_uri = connection_uri or os.getenv("SUPABASE_DB_URL")

    def apply(self) -> None:
        if not self.connection_uri:
            raise RuntimeError("Set SUPABASE_DB_URL (service role) to run migrations.")

        conn = psycopg2.connect(self.connection_uri)
        try:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
            conn.commit()
        finally:
            conn.close()

    def ddl(self) -> str:
        return SCHEMA_SQL


class SupabaseLoader:
    """Loads normalized ingestion artifacts into Supabase tables."""

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
    ) -> None:
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise RuntimeError("Supabase URL/key not configured.")
        self.client: Client = create_client(url, key)

    # ---------------------- PUBLIC API ----------------------
    def load_normalized(self, normalized_path: str) -> Dict[str, int]:
        with open(normalized_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        player_count = self.upsert_players(payload.get("players", {}).values())
        match_count = self.upsert_matches(payload.get("matches", {}).values())
        pm_count = self.upsert_player_matches(payload.get("player_matches", []))
        return {
            "players": player_count,
            "matches": match_count,
            "player_matches": pm_count,
        }

    def upsert_players(self, players: Iterable[Dict]) -> int:
        records = list(players)
        if not records:
            return 0
        self.client.table("players").upsert(records, on_conflict="account_id").execute()
        return len(records)

    def upsert_matches(self, matches: Iterable[Dict]) -> int:
        records = list(matches)
        if not records:
            return 0
        self.client.table("matches").upsert(records, on_conflict="match_id").execute()
        return len(records)

    def upsert_player_matches(self, player_matches: Iterable[Dict]) -> int:
        records = list(player_matches)
        if not records:
            return 0

        # Chunk to avoid exceeding Supabase payload limits
        chunk_size = 500
        for start in range(0, len(records), chunk_size):
            chunk = records[start : start + chunk_size]
            self.client.table("player_matches").upsert(
                chunk, on_conflict="account_id,match_id"
            ).execute()
        return len(records)

    # ---------------------- REFERENCE LOADING (OPTIONAL) ----------------------
    def load_reference_data(
        self, heroes: Optional[List[Dict]] = None, items: Optional[Dict[str, Dict]] = None
    ) -> None:
        if heroes:
            self._ensure_table("heroes", "id integer primary key, localized_name text, name text")
            hero_records = [
                {"id": hero.get("id"), "localized_name": hero.get("localized_name"), "name": hero.get("name")}
                for hero in heroes
            ]
            self.client.table("heroes").upsert(hero_records, on_conflict="id").execute()

        if items:
            self._ensure_table("items", "id serial primary key, key text unique, localized_name text")
            item_records = [
                {"key": key, "localized_name": value.get("dname")}
                for key, value in items.items()
            ]
            self.client.table("items").upsert(item_records, on_conflict="key").execute()

    def _ensure_table(self, table_name: str, definition: str) -> None:
        sql = f"CREATE TABLE IF NOT EXISTS public.{table_name} ({definition});"
        try:
            if hasattr(self.client, "postgrest"):
                self.client.postgrest.rpc("sql", {"query": sql}).execute()
        except Exception:
            # RPC sql function may not be available; in that case rely on schema.apply()
            pass

