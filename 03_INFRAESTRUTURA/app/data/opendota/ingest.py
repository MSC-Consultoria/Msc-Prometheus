"""Tournament ingestion helpers for OpenDota.

This module downloads league matches, persists XML archives (per match
and per player) and emits normalized JSON artifacts that can be loaded
into Supabase.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set

from .client import OpenDotaClient, save_xml


class TournamentIngestor:
    """Download and normalize OpenDota data for a tournament/league."""

    def __init__(self, client: OpenDotaClient, output_dir: str = "data/opendota"):
        self.client = client
        self.output_dir = Path(output_dir)
        self.matches_dir = self.output_dir / "matches"
        self.players_dir = self.output_dir / "players"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------- PUBLIC API ----------------------
    def ingest(
        self,
        league_id: int,
        player_match_limit: int = 500,
        pro_only: bool = True,
    ) -> Dict:
        """Run the full ingestion for a league.

        Returns a metadata dict with file locations and normalization
        stats. Artifacts are written under ``output_dir``.
        """

        league_matches = self.client.get_league_matches(league_id)
        player_ids: Set[int] = set()
        normalized = {
            "players": {},
            "matches": {},
            "player_matches": [],
        }

        for raw_match in league_matches:
            match_id = raw_match.get("match_id")
            if not match_id:
                continue
            match_payload = self.client.get_match(match_id)
            self._persist_match(match_payload)
            normalized["matches"][str(match_id)] = self._normalize_match(match_payload)

            for player in match_payload.get("players", []):
                account_id = player.get("account_id")
                if account_id:
                    player_ids.add(account_id)

        for account_id in sorted(player_ids):
            profile, player_matches = self._persist_player(account_id, player_match_limit, pro_only)
            normalized["players"][str(account_id)] = profile
            normalized["player_matches"].extend(
                [self._normalize_player_match(account_id, pm) for pm in player_matches]
            )

        normalized_path = self.output_dir / "normalized.json"
        with open(normalized_path, "w", encoding="utf-8") as handle:
            json.dump(normalized, handle, ensure_ascii=False, indent=2)

        metadata = {
            "league_id": league_id,
            "generated_at": datetime.utcnow().isoformat(),
            "output_dir": str(self.output_dir),
            "match_count": len(league_matches),
            "player_count": len(player_ids),
            "normalized_file": str(normalized_path),
            "xml": {
                "matches": str(self.matches_dir),
                "players": str(self.players_dir),
            },
        }

        with open(self.output_dir / "metadata.json", "w", encoding="utf-8") as handle:
            json.dump(metadata, handle, ensure_ascii=False, indent=2)

        return metadata

    # ---------------------- INTERNAL HELPERS ----------------------
    def _persist_match(self, match_payload: Dict) -> None:
        match_id = match_payload.get("match_id", "unknown")
        target = self.matches_dir / f"{match_id}.xml"
        save_xml(str(target), "match", match_payload)

    def _persist_player(
        self, account_id: int, match_limit: int, pro_only: bool
    ) -> tuple[Dict, List[Dict]]:
        profile = self.client.get_player(account_id)
        player_matches = self.client.get_player_matches(account_id, limit=match_limit, is_pro=pro_only)

        profile_path = self.players_dir / str(account_id) / "profile.xml"
        matches_path = self.players_dir / str(account_id) / "matches.xml"

        save_xml(str(profile_path), "player", profile)
        save_xml(str(matches_path), "matches", player_matches)

        return self._normalize_player_profile(account_id, profile), player_matches

    def _normalize_match(self, payload: Dict) -> Dict:
        return {
            "match_id": payload.get("match_id"),
            "duration": payload.get("duration"),
            "start_time": payload.get("start_time"),
            "radiant_win": payload.get("radiant_win"),
            "radiant_score": payload.get("radiant_score"),
            "dire_score": payload.get("dire_score"),
            "tower_status_radiant": payload.get("tower_status_radiant"),
            "tower_status_dire": payload.get("tower_status_dire"),
            "leagueid": payload.get("leagueid"),
            "cluster": payload.get("cluster"),
            "game_mode": payload.get("game_mode"),
            "engine": payload.get("engine"),
        }

    def _normalize_player_profile(self, account_id: int, payload: Dict) -> Dict:
        return {
            "account_id": account_id,
            "personaname": payload.get("profile", {}).get("personaname"),
            "name": payload.get("profile", {}).get("name"),
            "avatarfull": payload.get("profile", {}).get("avatarfull"),
            "last_login": payload.get("profile", {}).get("last_login"),
            "rank_tier": payload.get("rank_tier"),
            "leaderboard_rank": payload.get("leaderboard_rank"),
            "mmr_estimate": payload.get("mmr_estimate", {}).get("estimate"),
            "tracked_until": payload.get("tracked_until"),
        }

    def _normalize_player_match(self, account_id: int, payload: Dict) -> Dict:
        return {
            "account_id": account_id,
            "match_id": payload.get("match_id"),
            "player_slot": payload.get("player_slot"),
            "hero_id": payload.get("hero_id"),
            "kills": payload.get("kills"),
            "deaths": payload.get("deaths"),
            "assists": payload.get("assists"),
            "gold_per_min": payload.get("gold_per_min"),
            "xp_per_min": payload.get("xp_per_min"),
            "last_hits": payload.get("last_hits"),
            "denies": payload.get("denies"),
            "hero_damage": payload.get("hero_damage"),
            "tower_damage": payload.get("tower_damage"),
            "hero_healing": payload.get("hero_healing"),
            "duration": payload.get("duration"),
            "start_time": payload.get("start_time"),
            "lane": payload.get("lane"),
            "lane_role": payload.get("lane_role"),
            "is_roaming": payload.get("is_roaming"),
            "is_radiant": payload.get("is_radiant"),
            "win": payload.get("win"),
            "leaver_status": payload.get("leaver_status"),
            "party_size": payload.get("party_size"),
            "item_0": payload.get("item_0"),
            "item_1": payload.get("item_1"),
            "item_2": payload.get("item_2"),
            "item_3": payload.get("item_3"),
            "item_4": payload.get("item_4"),
            "item_5": payload.get("item_5"),
            "backpack_0": payload.get("backpack_0"),
            "backpack_1": payload.get("backpack_1"),
            "backpack_2": payload.get("backpack_2"),
        }


def run_ingestion(
    league_id: int,
    output_dir: str = "data/opendota",
    player_match_limit: int = 500,
    api_key: Optional[str] = None,
) -> Dict:
    """Convenience function for CLI/notebook usage."""

    client = OpenDotaClient(api_key=api_key)
    ingestor = TournamentIngestor(client=client, output_dir=output_dir)
    return ingestor.ingest(league_id=league_id, player_match_limit=player_match_limit)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="OpenDota league ingestor")
    parser.add_argument("league_id", type=int, help="ID da liga/campeonato no OpenDota")
    parser.add_argument("--output", default="data/opendota", help="Diretório de saída")
    parser.add_argument(
        "--limit", type=int, default=500, help="Limite de partidas por jogador"
    )
    args = parser.parse_args()

    metadata = run_ingestion(
        league_id=args.league_id, output_dir=args.output, player_match_limit=args.limit
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":  # pragma: no cover
    _cli()

