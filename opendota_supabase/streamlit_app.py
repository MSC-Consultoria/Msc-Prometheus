from datetime import datetime
from typing import List

import pandas as pd
import streamlit as st
from supabase import Client, create_client

from opendota_supabase.config import Settings, settings

st.set_page_config(page_title="OpenDota x Supabase", layout="wide")


def _get_settings() -> Settings:
    if not settings.supabase_url or not (settings.supabase_anon_key or settings.supabase_service_key):
        st.error("Configure SUPABASE_URL and SUPABASE_ANON_KEY in your environment.")
    return settings


@st.cache_resource(show_spinner=False)
def get_client(app_settings: Settings) -> Client:
    api_key = app_settings.supabase_anon_key or app_settings.supabase_service_key
    return create_client(app_settings.supabase_url, api_key)


@st.cache_data(ttl=300, show_spinner=False)
def load_matches(client: Client, table: str, limit: int = 50) -> pd.DataFrame:
    response = (
        client.table(table)
        .select("match_id, player_id, hero_id, kills, deaths, assists, duration, player_slot, radiant_win, start_time")
        .order("start_time", desc=True)
        .limit(limit)
        .execute()
    )
    data = response.data or []
    frame = pd.DataFrame(data)
    if not frame.empty:
        frame["start_time"] = frame["start_time"].apply(_format_timestamp)
        frame["result"] = frame.apply(_get_result, axis=1)
    return frame


@st.cache_data(ttl=300, show_spinner=False)
def load_players(client: Client, table: str) -> pd.DataFrame:
    response = (
        client.table(table)
        .select("player_id, personaname, mmr, rank_tier, profile_url, avatar, last_login")
        .order("personaname")
        .execute()
    )
    data = response.data or []
    frame = pd.DataFrame(data)
    if not frame.empty and "last_login" in frame:
        frame["last_login"] = frame["last_login"].apply(_format_timestamp)
    return frame


def _get_result(row: pd.Series) -> str:
    if pd.isna(row.get("player_slot")) or pd.isna(row.get("radiant_win")):
        return ""
    is_radiant = int(row["player_slot"]) < 128
    won = bool(row["radiant_win"]) if is_radiant else not bool(row["radiant_win"])
    return "Win" if won else "Loss"


def _format_timestamp(value) -> str:
    if not value:
        return ""
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M")
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return str(value)


def render_summary(matches: pd.DataFrame, players: pd.DataFrame) -> None:
    cols = st.columns(3)
    total = len(matches)
    wins = len(matches[matches["result"] == "Win"])
    win_rate = (wins / total * 100) if total else 0
    cols[0].metric("Matches", f"{total}")
    cols[1].metric("Wins", f"{wins}")
    cols[2].metric("Win rate", f"{win_rate:.1f}%")

    st.markdown("### Players")
    st.dataframe(
        players[["player_id", "personaname", "mmr", "rank_tier", "last_login"]],
        use_container_width=True,
        hide_index=True,
    )



def render_recent_matches(matches: pd.DataFrame, players: pd.DataFrame) -> None:
    st.markdown("### Recent matches")
    if matches.empty:
        st.info("No matches found. Run the ETL to pull data from OpenDota.")
        return

    player_map = {
        row.player_id: row.personaname or row.player_id for _, row in players.iterrows()
    }

    matches = matches.copy()
    matches["player"] = matches["player_id"].map(player_map)
    st.dataframe(
        matches[
            [
                "match_id",
                "player",
                "hero_id",
                "result",
                "kills",
                "deaths",
                "assists",
                "duration",
                "start_time",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )



def main() -> None:
    app_settings = _get_settings()
    client = get_client(app_settings)

    st.title("OpenDota → Supabase dashboard")
    st.caption("Monitor player stats synced from OpenDota via the ETL job.")

    players = load_players(client, app_settings.players_table)
    matches = load_matches(client, app_settings.matches_table)

    with st.sidebar:
        st.header("Filters")
        selected_players: List[str] = st.multiselect(
            "Players",
            options=players["player_id"].tolist() if not players.empty else [],
            default=players["player_id"].tolist() if not players.empty else [],
        )
        if selected_players and not matches.empty:
            matches = matches[matches["player_id"].isin(selected_players)]

        st.divider()
        st.markdown("#### Health check")
        st.markdown("`/healthz` on the nginx service returns HTTP 200 for uptime checks.")

    render_summary(matches, players)
    render_recent_matches(matches, players)


if __name__ == "__main__":
    main()
