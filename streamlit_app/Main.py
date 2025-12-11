import os
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import altair as alt
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import Client, ClientOptions, create_client


load_dotenv()
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "600"))
CACHE_HASH_FUNCS = {Client: lambda _: "supabase-client"}

st.set_page_config(
    page_title="Prometheus | Pro Match Insights",
    layout="wide",
    page_icon="📊",
)


@dataclass
class AppConfig:
    supabase_url: str
    supabase_key: str
    schema: Optional[str] = None
    tournaments_table: str = "tournaments"
    teams_table: str = "teams"
    players_table: str = "players"
    matches_table: str = "pro_matches"
    cache_ttl: int = CACHE_TTL


@st.cache_resource(show_spinner=False)
def get_supabase_client(url: str, key: str, schema: Optional[str]) -> Client:
    headers = {"Accept-Profile": schema} if schema else None
    options = ClientOptions(headers=headers) if headers else None
    return create_client(url, key, options=options)


def load_config() -> AppConfig:
    return AppConfig(
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY", ""),
        schema=os.getenv("SUPABASE_SCHEMA"),
        tournaments_table=os.getenv("SUPABASE_TOURNAMENTS_TABLE", "tournaments"),
        teams_table=os.getenv("SUPABASE_TEAMS_TABLE", "teams"),
        players_table=os.getenv("SUPABASE_PLAYERS_TABLE", "players"),
        matches_table=os.getenv("SUPABASE_PRO_MATCHES_TABLE", "pro_matches"),
        cache_ttl=CACHE_TTL,
    )


def _safe_execute(query: Any) -> List[Dict[str, Any]]:
    try:
        response = query.execute()
        return response.data or []
    except Exception as exc:  # noqa: BLE001
        st.error(f"Supabase query failed: {exc}")
        return []


@st.cache_data(show_spinner=False, ttl=CACHE_TTL, hash_funcs=CACHE_HASH_FUNCS)
def load_tournaments(client: Client, table: str) -> List[Dict[str, Any]]:
    query = client.table(table).select("id,name,start_date").order("start_date", desc=True)
    return _safe_execute(query)


@st.cache_data(show_spinner=False, ttl=CACHE_TTL, hash_funcs=CACHE_HASH_FUNCS)
def load_teams(client: Client, table: str, tournament_id: Optional[str]) -> List[Dict[str, Any]]:
    query = client.table(table).select("id,name,tournament_id")
    if tournament_id:
        query = query.eq("tournament_id", tournament_id)
    query = query.order("name")
    return _safe_execute(query)


@st.cache_data(show_spinner=False, ttl=CACHE_TTL, hash_funcs=CACHE_HASH_FUNCS)
def load_players(
    client: Client,
    table: str,
    tournament_id: Optional[str],
    team_id: Optional[str],
) -> List[Dict[str, Any]]:
    query = client.table(table).select("id,name,position,team_id,tournament_id").order("name")
    if tournament_id:
        query = query.eq("tournament_id", tournament_id)
    if team_id:
        query = query.eq("team_id", team_id)
    return _safe_execute(query)


@st.cache_data(show_spinner=False, ttl=CACHE_TTL, hash_funcs=CACHE_HASH_FUNCS)
def load_heroes(client: Client) -> List[Dict[str, Any]]:
    query = client.table("heroes").select("id,name,primary_attr").order("name")
    return _safe_execute(query)


@st.cache_data(show_spinner=False, ttl=CACHE_TTL, hash_funcs=CACHE_HASH_FUNCS)
def load_player_matches(
    client: Client,
    table: str,
    player_id: str,
    tournament_id: Optional[str],
    hero_id: Optional[str],
) -> List[Dict[str, Any]]:
    query = (
        client.table(table)
        .select("*")
        .eq("player_id", player_id)
        .order("match_date", desc=True)
        .limit(500)
    )
    if tournament_id:
        query = query.eq("tournament_id", tournament_id)
    if hero_id:
        query = query.eq("hero_id", hero_id)
    return _safe_execute(query)


def compute_kpis(matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    totals = {"kills": 0, "deaths": 0, "assists": 0, "gpm": 0.0, "xpm": 0.0}
    hero_counts: Dict[str, Dict[str, int]] = {}
    item_timings: Dict[str, List[float]] = {}

    for match in matches:
        totals["kills"] += match.get("kills", 0)
        totals["deaths"] += match.get("deaths", 0)
        totals["assists"] += match.get("assists", 0)
        totals["gpm"] += match.get("gpm", 0.0)
        totals["xpm"] += match.get("xpm", 0.0)

        hero_id = match.get("hero_id")
        if hero_id is not None:
            hero_key = str(hero_id)
            hero_counts.setdefault(hero_key, {"matches": 0, "wins": 0})
            hero_counts[hero_key]["matches"] += 1
            if match.get("win"):
                hero_counts[hero_key]["wins"] += 1

        for timing in match.get("item_timings", []):
            item = timing.get("item")
            time_seconds = timing.get("time")
            if not item or time_seconds is None:
                continue
            item_timings.setdefault(item, []).append(float(time_seconds))

    match_count = max(len(matches), 1)
    deaths = totals["deaths"] if totals["deaths"] > 0 else 1
    hero_pool = [
        {
            "hero_id": hero,
            "matches": stats["matches"],
            "win_rate": round((stats["wins"] / stats["matches"]) * 100, 1) if stats["matches"] else 0.0,
        }
        for hero, stats in hero_counts.items()
    ]
    hero_pool.sort(key=lambda entry: entry["matches"], reverse=True)

    avg_item_timings = [
        {"item": item, "avg_purchase_time": round(sum(times) / len(times), 1)}
        for item, times in item_timings.items()
    ]
    avg_item_timings.sort(key=lambda entry: entry["avg_purchase_time"])

    return {
        "kda": round((totals["kills"] + totals["assists"]) / deaths, 2),
        "gpm": round(totals["gpm"] / match_count, 1),
        "xpm": round(totals["xpm"] / match_count, 1),
        "item_timings": avg_item_timings[:10],
        "hero_pool": hero_pool[:10],
    }


def render_kpi_cards(kpis: Dict[str, Any]):
    col1, col2, col3 = st.columns(3)
    col1.metric("KDA", kpis["kda"])
    col2.metric("Avg. GPM", kpis["gpm"])
    col3.metric("Avg. XPM", kpis["xpm"])

    col4, col5 = st.columns(2)
    col4.subheader("Fastest Item Timings")
    col4.dataframe(pd.DataFrame(kpis["item_timings"]))

    col5.subheader("Top Hero Pool")
    hero_df = pd.DataFrame(kpis["hero_pool"])
    if not hero_df.empty:
        col5.bar_chart(hero_df.set_index("hero_id")["win_rate"], use_container_width=True)
    else:
        col5.info("No hero data available yet.")


def build_trend_charts(matches: List[Dict[str, Any]]):
    if not matches:
        st.info("No matches to chart yet. Select a player to load data.")
        return

    df = pd.DataFrame(matches)
    if "match_date" in df.columns:
        df["match_date"] = pd.to_datetime(df["match_date"])
    else:
        df["match_date"] = pd.RangeIndex(len(df))

    df = df.sort_values("match_date")
    line_cols = st.columns(2)

    with line_cols[0]:
        st.subheader("Performance Trend (Kills / Deaths / Assists)")
        perf_cols = [col for col in ["kills", "deaths", "assists"] if col in df.columns]
        if perf_cols:
            st.line_chart(df.set_index("match_date")[perf_cols], use_container_width=True)
        else:
            st.info("Kills, deaths, and assists are not available for this selection.")

    with line_cols[1]:
        st.subheader("Economy Trend (GPM / XPM)")
        econ_cols = [col for col in ["gpm", "xpm"] if col in df.columns]
        if econ_cols:
            st.line_chart(df.set_index("match_date")[econ_cols], use_container_width=True)
        else:
            st.info("Economy metrics are not available for this selection.")


def _ensure_interval_rows(match: Dict[str, Any]) -> List[Dict[str, Any]]:
    intervals = match.get("interval_stats") or []
    if intervals:
        return intervals

    duration = match.get("duration") or 0
    bucket = max(int(duration / 5), 1)
    return [
        {
            "interval": f"0-{bucket} min",
            "kills": match.get("kills", 0),
            "deaths": match.get("deaths", 0),
            "assists": match.get("assists", 0),
        }
    ]


def render_match_details(match: Dict[str, Any]):
    st.markdown("---")
    st.subheader(f"Match {match.get('id') or match.get('match_id')}")
    meta_cols = st.columns(4)
    meta_cols[0].metric("Result", "Win" if match.get("win") else "Loss")
    meta_cols[1].metric("Duration (min)", round((match.get("duration", 0) or 0) / 60, 1))
    meta_cols[2].metric("Hero", str(match.get("hero_id", "-")))
    meta_cols[3].metric("Opponent", match.get("opponent", "-"))

    st.markdown("### Item Purchase Timeline")
    purchases = match.get("item_purchases") or match.get("item_timings") or []
    if purchases:
        purchase_df = pd.DataFrame(purchases)
        purchase_df.rename(columns={"time": "seconds"}, inplace=True)
        if "seconds" not in purchase_df:
            purchase_df["seconds"] = 0
        purchase_df["minutes"] = (purchase_df["seconds"].astype(float) / 60).round(1)
        if "item" not in purchase_df:
            purchase_df["item"] = "Unknown"
        purchase_df["item"] = purchase_df["item"].fillna("Unknown")
        timeline = (
            alt.Chart(purchase_df)
            .mark_circle(size=120)
            .encode(
                x=alt.X("minutes:Q", title="Minute"),
                y=alt.Y("item:N", title="Item"),
                color=alt.Color("minutes:Q", title="Timing", scale=alt.Scale(scheme="plasma")),
                tooltip=["item", "minutes"],
            )
        )
        st.altair_chart(timeline, use_container_width=True)
    else:
        st.info("No item purchase data available for this match.")

    st.markdown("### Interval K/D/A")
    interval_rows = _ensure_interval_rows(match)
    interval_df = pd.DataFrame(interval_rows)
    interval_df.set_index("interval", inplace=True)
    st.bar_chart(interval_df[["kills", "deaths", "assists"]], use_container_width=True)

    st.markdown("### Hero Performance Summary")
    hero_summary = {
        "hero_id": match.get("hero_id"),
        "lane": match.get("lane"),
        "kda": f"{match.get('kills', 0)}/{match.get('deaths', 0)}/{match.get('assists', 0)}",
        "gpm": match.get("gpm"),
        "xpm": match.get("xpm"),
        "last_hits": match.get("last_hits"),
        "denies": match.get("denies"),
    }
    st.table(pd.DataFrame([hero_summary]))

    export_df = interval_df.reset_index()
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")
    xml_bytes = dataframe_to_xml(export_df)

    dl_cols = st.columns(2)
    dl_cols[0].download_button(
        label="Download match intervals (CSV)",
        data=csv_bytes,
        file_name=f"match_{match.get('match_id', match.get('id', 'detail'))}_intervals.csv",
        mime="text/csv",
    )
    dl_cols[1].download_button(
        label="Download match intervals (XML)",
        data=xml_bytes,
        file_name=f"match_{match.get('match_id', match.get('id', 'detail'))}_intervals.xml",
        mime="application/xml",
    )


def dataframe_to_xml(df: pd.DataFrame) -> bytes:
    rows = []
    for _, row in df.iterrows():
        fields = "".join([f"    <{col}>{row[col]}</{col}>" for col in df.columns])
        rows.append(f"  <row>\n{fields}\n  </row>")
    xml_body = "\n".join(rows)
    xml_string = f"<?xml version='1.0' encoding='UTF-8'?>\n<data>\n{xml_body}\n</data>"
    return xml_string.encode("utf-8")


def render_dashboard():
    config = load_config()
    if not config.supabase_url or not config.supabase_key:
        st.error("Supabase URL and KEY are required. Set SUPABASE_URL and SUPABASE_ANON_KEY/SERVICE_ROLE_KEY in the environment.")
        return

    client = get_supabase_client(config.supabase_url, config.supabase_key, config.schema)

    tournaments = load_tournaments(client, config.tournaments_table)
    tournament_options = {t.get("name", "Unnamed"): t.get("id") for t in tournaments}
    selected_tournament = st.sidebar.selectbox("Tournament", list(tournament_options.keys())) if tournaments else None
    selected_tournament_id = tournament_options.get(selected_tournament) if selected_tournament else None

    teams = load_teams(client, config.teams_table, selected_tournament_id)
    team_options = {t.get("name", "Team"): t.get("id") for t in teams}
    selected_team = st.sidebar.selectbox("Team", list(team_options.keys())) if teams else None
    selected_team_id = team_options.get(selected_team) if selected_team else None

    players = load_players(client, config.players_table, selected_tournament_id, selected_team_id)
    player_options = {p.get("name", "Player"): p.get("id") for p in players}
    selected_player = st.sidebar.selectbox("Player", list(player_options.keys())) if players else None
    selected_player_id = player_options.get(selected_player) if selected_player else None

    heroes = load_heroes(client)
    hero_options = {h.get("name", "Hero"): h.get("id") for h in heroes}
    selected_hero = st.sidebar.selectbox("Hero", ["All"] + list(hero_options.keys())) if heroes else "All"
    selected_hero_id = None if selected_hero == "All" else hero_options.get(selected_hero)

    st.title("Pro Match Insights")
    st.caption("KPIs and detailed timelines powered by Supabase with cached queries for fast browsing.")

    if not selected_player_id:
        st.info("Select a tournament, team, and player to view metrics.")
        return

    matches = load_player_matches(
        client,
        config.matches_table,
        selected_player_id,
        selected_tournament_id,
        selected_hero_id,
    )

    if not matches:
        st.warning("No pro matches found for this player with the selected filters.")
        return

    kpis = compute_kpis(matches)
    render_kpi_cards(kpis)
    build_trend_charts(matches)

    st.markdown("## Match Details")
    match_options = {
        f"{m.get('match_date', '')} • {m.get('opponent', 'vs ?')} ({'W' if m.get('win') else 'L'})": m
        for m in matches
    }
    selected_match_label = st.selectbox("Select a match", list(match_options.keys()))
    render_match_details(match_options[selected_match_label])


if __name__ == "__main__":
    render_dashboard()
