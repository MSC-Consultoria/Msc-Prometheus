"""Streamlit prototype to explore OpenDota league data stored in Supabase."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import pandas as pd
import streamlit as st
from supabase import Client, create_client

PAGE_TITLE = "OpenDota • Supabase • Streamlit"


def _build_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("Configure SUPABASE_URL and SUPABASE_ANON_KEY/SERVICE_KEY.")
    return create_client(url, key)


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title(PAGE_TITLE)
    st.caption("Dashboard protótipo para explorar métricas do campeonato no Supabase")

    try:
        client = st.cache_resource(_build_client)()
    except Exception as exc:  # pragma: no cover - UI feedback only
        st.error(f"Erro ao conectar no Supabase: {exc}")
        st.stop()

    players_df = load_table(client, "players")
    matches_df = load_table(client, "matches")
    player_matches_df = load_table(client, "player_matches")

    if players_df.empty or matches_df.empty or player_matches_df.empty:
        st.info("Nenhum dado carregado ainda. Rode o pipeline de ingestão primeiro.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jogadores", f"{len(players_df):,}")
    with col2:
        st.metric("Partidas", f"{len(matches_df):,}")
    with col3:
        avg_kda = compute_average_kda(player_matches_df)
        st.metric("KDA médio", f"{avg_kda:.2f}")

    st.divider()
    left, right = st.columns([1, 2])
    with left:
        selected_player = st.selectbox(
            "Jogador",
            options=players_df.sort_values("personaname")["account_id"],
            format_func=lambda pid: players_df.loc[
                players_df["account_id"] == pid, "personaname"
            ].values[0],
        )
        filtered = player_matches_df[player_matches_df["account_id"] == selected_player]
        st.write("Últimas partidas (pro)", filtered.head(30))
    with right:
        st.subheader("Curvas de desempenho")
        if not filtered.empty:
            filtered_sorted = filtered.sort_values("start_time")
            st.line_chart(
                filtered_sorted.set_index("start_time")[[
                    "kills",
                    "deaths",
                    "assists",
                    "gold_per_min",
                    "xp_per_min",
                ]]
            )

    st.divider()
    st.subheader("Heróis mais usados")
    top_heroes = (
        player_matches_df.groupby("hero_id")["match_id"].count().reset_index().rename(columns={"match_id": "partidas"})
    )
    st.dataframe(top_heroes.sort_values("partidas", ascending=False).head(25))


def load_table(client: Client, table: str) -> pd.DataFrame:
    response = client.table(table).select("*").execute()
    data: List[Dict[str, Any]] = response.data or []
    return pd.DataFrame(data)


def compute_average_kda(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    kills = df["kills"].fillna(0)
    assists = df["assists"].fillna(0)
    deaths = df["deaths"].replace(0, 1)  # avoid div by zero
    kda = (kills + assists) / deaths
    return float(kda.mean())


if __name__ == "__main__":  # pragma: no cover
    main()

