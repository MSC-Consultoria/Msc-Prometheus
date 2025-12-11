from datetime import datetime
from typing import Any, Dict, Iterable, List

import requests
from supabase import Client, create_client

from opendota_supabase.config import Settings, settings


class OpenDotaETL:
    """Extract, transform and load OpenDota player data into Supabase."""

    def __init__(self, app_settings: Settings | None = None):
        self.settings = app_settings or settings
        self.settings.validate()
        self.supabase: Client = create_client(
            self.settings.supabase_url, self.settings.supabase_service_key
        )

    def _request_params(self) -> Dict[str, str]:
        if self.settings.opendota_api_key:
            return {"api_key": self.settings.opendota_api_key}
        return {}

    def fetch_recent_matches(self, player_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        response = requests.get(
            f"https://api.opendota.com/api/players/{player_id}/recentMatches",
            params={"limit": limit, **self._request_params()},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def fetch_player_profile(self, player_id: str) -> Dict[str, Any]:
        response = requests.get(
            f"https://api.opendota.com/api/players/{player_id}",
            params=self._request_params(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def _transform_match(self, player_id: str, match: Dict[str, Any]) -> Dict[str, Any]:
        start_time = match.get("start_time")
        start_time_iso = (
            datetime.utcfromtimestamp(start_time).isoformat() + "Z" if start_time else None
        )
        return {
            "match_id": match.get("match_id"),
            "player_id": player_id,
            "hero_id": match.get("hero_id"),
            "kills": match.get("kills"),
            "deaths": match.get("deaths"),
            "assists": match.get("assists"),
            "duration": match.get("duration"),
            "player_slot": match.get("player_slot"),
            "radiant_win": match.get("radiant_win"),
            "start_time": start_time_iso,
        }

    def _transform_player(self, player_id: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        profile_data = profile.get("profile", {})
        last_login = profile_data.get("last_login")
        return {
            "player_id": player_id,
            "personaname": profile_data.get("personaname"),
            "name": profile_data.get("name"),
            "mmr": profile.get("mmr_estimate", {}).get("estimate"),
            "rank_tier": profile.get("rank_tier"),
            "profile_url": profile_data.get("profileurl"),
            "avatar": profile_data.get("avatarfull"),
            "last_login": last_login,
        }

    def load_matches(self, matches: Iterable[Dict[str, Any]]) -> None:
        records = [m for m in matches if m.get("match_id")]
        if not records:
            return
        self.supabase.table(self.settings.matches_table).upsert(records, on_conflict="match_id").execute()

    def load_players(self, players: Iterable[Dict[str, Any]]) -> None:
        records = [p for p in players if p.get("player_id")]
        if not records:
            return
        self.supabase.table(self.settings.players_table).upsert(records, on_conflict="player_id").execute()

    def run(self, match_limit: int = 20) -> None:
        if not self.settings.player_ids:
            raise ValueError("No player ids configured. Add OPENDOTA_PLAYER_IDS to your environment.")

        transformed_matches: List[Dict[str, Any]] = []
        transformed_players: List[Dict[str, Any]] = []

        for player_id in self.settings.player_ids:
            player_profile = self.fetch_player_profile(player_id)
            transformed_players.append(self._transform_player(player_id, player_profile))

            recent_matches = self.fetch_recent_matches(player_id, limit=match_limit)
            transformed_matches.extend(
                [self._transform_match(player_id, match) for match in recent_matches]
            )

        self.load_players(transformed_players)
        self.load_matches(transformed_matches)


if __name__ == "__main__":
    etl = OpenDotaETL()
    etl.run()
