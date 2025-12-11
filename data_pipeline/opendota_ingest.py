"""
OpenDota ETL pipeline for tournament ingestion.

Usage:
    python -m data_pipeline.opendota_ingest --tournament <id> --out data/raw_xml
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd
import requests

LOGGER = logging.getLogger(__name__)
DEFAULT_BASE_URL = os.getenv("OPENDOTA_BASE_URL", "https://api.opendota.com/api")
DEFAULT_API_KEY = os.getenv("OPENDOTA_API_KEY")


@dataclass
class Purchase:
    match_id: int
    account_id: Optional[int]
    time: Optional[int]
    item: str


@dataclass
class IntervalKDA:
    match_id: int
    account_id: Optional[int]
    interval_start: int
    kills: int
    deaths: int
    assists: int


@dataclass
class PlayerPerformance:
    match_id: int
    account_id: Optional[int]
    hero_id: Optional[int]
    lane: Optional[int]
    lane_role: Optional[int]
    is_roaming: Optional[int]
    kills: int
    deaths: int
    assists: int
    gpm: int
    xpm: int
    hero_damage: int
    tower_damage: int
    hero_healing: int
    last_hits: int
    denies: int
    gold: int
    xp_per_min: int
    level: int
    kda: Optional[float]
    items: Dict[str, Optional[int]]


class OpenDotaClient:
    def __init__(
        self,
        api_key: Optional[str] = DEFAULT_API_KEY,
        base_url: str = DEFAULT_BASE_URL,
        max_retries: int = 5,
        backoff_factor: float = 1.5,
        rate_limit_sleep: int = 3,
        timeout: int = 30,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.rate_limit_sleep = rate_limit_sleep
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"
        params = params.copy() if params else {}
        if self.api_key:
            params.setdefault("api_key", self.api_key)

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    params=params,
                    timeout=self.timeout,
                )
                if response.status_code == 429:
                    sleep_time = self.rate_limit_sleep * attempt
                    LOGGER.warning("Rate limited by OpenDota, sleeping for %s seconds", sleep_time)
                    time.sleep(sleep_time)
                    continue
                if response.status_code >= 500:
                    sleep_time = self.backoff_factor ** attempt
                    LOGGER.warning(
                        "Server error %s on %s. Retrying in %.1f seconds", response.status_code, url, sleep_time
                    )
                    time.sleep(sleep_time)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.RequestException as exc:  # type: ignore[attr-defined]
                sleep_time = self.backoff_factor ** attempt
                LOGGER.warning("Error calling %s: %s. Retrying in %.1f seconds", url, exc, sleep_time)
                if attempt == self.max_retries:
                    raise
                time.sleep(sleep_time)
        raise RuntimeError("Exceeded maximum retries")

    def get_tournament_match_ids(self, tournament_id: int) -> List[int]:
        LOGGER.info("Fetching match IDs for tournament %s", tournament_id)
        sql = f"SELECT match_id FROM matches WHERE leagueid={int(tournament_id)} ORDER BY start_time DESC"
        try:
            data = self._request("get", "/explorer", params={"sql": sql})
            rows = data.get("rows", []) if isinstance(data, dict) else []
            if rows:
                match_ids = [int(row["match_id"]) for row in rows if row.get("match_id")]
                LOGGER.info("Found %s match IDs via /explorer", len(match_ids))
                return match_ids
        except Exception:
            LOGGER.warning("Explorer endpoint unavailable, falling back to /proMatches")

        pro_matches = self._request("get", "/proMatches")
        match_ids = [int(match["match_id"]) for match in pro_matches if match.get("leagueid") == tournament_id]
        LOGGER.info("Found %s match IDs via /proMatches", len(match_ids))
        return match_ids

    def get_match(self, match_id: int) -> Dict[str, Any]:
        LOGGER.info("Fetching match details for %s", match_id)
        return self._request("get", f"/matches/{match_id}")

    def get_player_pro_matches(self, account_id: int, limit: int = 500) -> List[Dict[str, Any]]:
        LOGGER.debug("Fetching pro matches for player %s", account_id)
        data = self._request(
            "get",
            f"/players/{account_id}/matches",
            params={"limit": limit, "is_pro": 1, "significant": 0},
        )
        return data if isinstance(data, list) else []


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def dict_to_xml(tag: str, data: Any) -> Any:
    from xml.etree.ElementTree import Element, SubElement

    def build_element(parent: Element, key: str, value: Any) -> None:
        if isinstance(value, dict):
            child = SubElement(parent, key)
            for sub_key, sub_val in value.items():
                build_element(child, str(sub_key), sub_val)
        elif isinstance(value, list):
            list_parent = SubElement(parent, key)
            for idx, item in enumerate(value):
                build_element(list_parent, f"item_{idx}", item)
        else:
            child = SubElement(parent, key)
            child.text = str(value)

    root = Element(tag)
    if isinstance(data, dict):
        for key, value in data.items():
            build_element(root, str(key), value)
    else:
        build_element(root, "value", data)
    return root


def save_xml(path: Path, data: Dict[str, Any], root_tag: str) -> None:
    from xml.etree.ElementTree import ElementTree

    _ensure_dir(path.parent)
    tree = ElementTree(dict_to_xml(root_tag, data))
    tree.write(path, encoding="utf-8", xml_declaration=True)


def save_json(path: Path, data: Any) -> None:
    _ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)


def save_parquet(path: Path, data: pd.DataFrame) -> None:
    _ensure_dir(path.parent)
    if data.empty:
        LOGGER.warning("No data to save to %s", path)
        return
    data.to_parquet(path, index=False)


def bucket_event_log(events: Iterable[Dict[str, Any]], interval: int = 300) -> Dict[int, int]:
    buckets: Dict[int, int] = {}
    for event in events:
        event_time = event.get("time")
        if event_time is None:
            continue
        bucket = (int(event_time) // interval) * interval
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return buckets


def normalize_player(player: Dict[str, Any], match_id: int) -> Dict[str, Any]:
    account_id = player.get("account_id")
    purchases = [
        Purchase(
            match_id=match_id,
            account_id=account_id,
            time=item.get("time"),
            item=item.get("key", ""),
        )
        for item in player.get("purchase_log", [])
    ]

    kill_buckets = bucket_event_log(player.get("kills_log", []))
    death_buckets = bucket_event_log(player.get("deaths_log", []))
    assist_buckets: Dict[int, int] = bucket_event_log(player.get("assists_log", []))
    intervals = []
    for bucket in sorted(set(kill_buckets) | set(death_buckets) | set(assist_buckets)):
        intervals.append(
            IntervalKDA(
                match_id=match_id,
                account_id=account_id,
                interval_start=bucket,
                kills=kill_buckets.get(bucket, 0),
                deaths=death_buckets.get(bucket, 0),
                assists=assist_buckets.get(bucket, 0),
            )
        )

    items = {key: player.get(key) for key in [
        "item_0",
        "item_1",
        "item_2",
        "item_3",
        "item_4",
        "item_5",
        "backpack_0",
        "backpack_1",
        "backpack_2",
        "item_neutral",
    ]}

    performance = PlayerPerformance(
        match_id=match_id,
        account_id=account_id,
        hero_id=player.get("hero_id"),
        lane=player.get("lane"),
        lane_role=player.get("lane_role"),
        is_roaming=player.get("is_roaming"),
        kills=player.get("kills", 0),
        deaths=player.get("deaths", 0),
        assists=player.get("assists", 0),
        gpm=player.get("gold_per_min", 0),
        xpm=player.get("xp_per_min", 0),
        hero_damage=player.get("hero_damage", 0),
        tower_damage=player.get("tower_damage", 0),
        hero_healing=player.get("hero_healing", 0),
        last_hits=player.get("last_hits", 0),
        denies=player.get("denies", 0),
        gold=player.get("gold", 0),
        xp_per_min=player.get("xp_per_min", 0),
        level=player.get("level", 0),
        kda=player.get("kda"),
        items=items,
    )

    return {
        "raw": player,
        "purchases": purchases,
        "intervals": intervals,
        "performance": performance,
    }


def normalize_match(match: Dict[str, Any]) -> Dict[str, Any]:
    match_id = match.get("match_id")
    normalized_players = [normalize_player(player, match_id) for player in match.get("players", [])]

    return {
        "match_id": match_id,
        "start_time": match.get("start_time"),
        "duration": match.get("duration"),
        "radiant_win": match.get("radiant_win"),
        "leagueid": match.get("leagueid"),
        "players": normalized_players,
    }


def process_tournament(
    client: OpenDotaClient,
    tournament_id: int,
    output_dir: Path,
    max_matches: Optional[int] = None,
) -> None:
    raw_match_dir = output_dir / "raw_xml" / "matches"
    raw_player_dir = output_dir / "raw_xml" / "players"
    processed_dir = output_dir / "processed"

    match_ids = client.get_tournament_match_ids(tournament_id)
    if max_matches:
        match_ids = match_ids[:max_matches]

    matches_summary: List[Dict[str, Any]] = []
    performance_rows: List[Dict[str, Any]] = []
    purchase_rows: List[Dict[str, Any]] = []
    interval_rows: List[Dict[str, Any]] = []
    pro_match_rows: List[Dict[str, Any]] = []

    for match_id in match_ids:
        try:
            match_data = client.get_match(match_id)
        except Exception as exc:  # type: ignore[attr-defined]
            LOGGER.error("Failed to fetch match %s: %s", match_id, exc)
            continue

        save_xml(raw_match_dir / f"match_{match_id}.xml", match_data, root_tag="match")
        normalized = normalize_match(match_data)
        matches_summary.append({
            "match_id": match_id,
            "start_time": normalized.get("start_time"),
            "duration": normalized.get("duration"),
            "radiant_win": normalized.get("radiant_win"),
            "leagueid": normalized.get("leagueid"),
        })

        for player_block in normalized["players"]:
            player_raw = player_block["raw"]
            account_id = player_raw.get("account_id")
            save_xml(raw_player_dir / f"match_{match_id}_player_{account_id or 'anon'}.xml", player_raw, root_tag="player")

            performance_rows.append(asdict(player_block["performance"]))
            purchase_rows.extend(asdict(purchase) for purchase in player_block["purchases"])
            interval_rows.extend(asdict(interval) for interval in player_block["intervals"])

            if account_id:
                pro_matches = client.get_player_pro_matches(account_id)
                for pm in pro_matches:
                    pm["account_id"] = account_id
                    pm["source_match_id"] = match_id
                pro_match_rows.extend(pm for pm in pro_matches)

    if matches_summary:
        save_json(processed_dir / f"matches_tournament_{tournament_id}.json", matches_summary)
        save_parquet(processed_dir / f"matches_tournament_{tournament_id}.parquet", pd.DataFrame(matches_summary))

    if performance_rows:
        save_json(processed_dir / f"players_tournament_{tournament_id}.json", performance_rows)
        save_parquet(processed_dir / f"players_tournament_{tournament_id}.parquet", pd.DataFrame(performance_rows))

    if purchase_rows:
        save_json(processed_dir / f"purchases_tournament_{tournament_id}.json", purchase_rows)
        save_parquet(processed_dir / f"purchases_tournament_{tournament_id}.parquet", pd.DataFrame(purchase_rows))

    if interval_rows:
        save_json(processed_dir / f"intervals_tournament_{tournament_id}.json", interval_rows)
        save_parquet(processed_dir / f"intervals_tournament_{tournament_id}.parquet", pd.DataFrame(interval_rows))

    if pro_match_rows:
        save_json(processed_dir / f"pro_matches_from_tournament_{tournament_id}.json", pro_match_rows)
        save_parquet(
            processed_dir / f"pro_matches_from_tournament_{tournament_id}.parquet",
            pd.DataFrame(pro_match_rows),
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenDota ETL pipeline for tournaments")
    parser.add_argument("--tournament", type=int, required=True, help="Tournament/league ID to ingest")
    parser.add_argument("--out", type=Path, default=Path("data"), help="Base output directory")
    parser.add_argument("--base-url", type=str, default=DEFAULT_BASE_URL, help="OpenDota base URL")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY, help="Premium API key")
    parser.add_argument("--max-matches", type=int, default=None, help="Optional limit of matches to ingest")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    client = OpenDotaClient(api_key=args.api_key, base_url=args.base_url)
    process_tournament(client, args.tournament, args.out, max_matches=args.max_matches)


if __name__ == "__main__":
    main()
