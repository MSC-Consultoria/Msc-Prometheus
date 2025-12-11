-- Migration: foundational schema for match analytics
-- Creates normalized tables and materialized views for aggregated insights

-- Enable useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Base entities
CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    rank_tier TEXT,
    region TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS heroes (
    hero_id INTEGER PRIMARY KEY,
    hero_name TEXT NOT NULL,
    primary_attribute TEXT,
    roles TEXT[]
);

CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    item_type TEXT,
    cost INTEGER,
    lore TEXT
);

CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    duration_seconds INTEGER NOT NULL,
    game_mode TEXT,
    patch_version TEXT,
    radiant_win BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS player_matches (
    player_id TEXT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    match_id TEXT NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    hero_id INTEGER REFERENCES heroes(hero_id),
    team TEXT,
    role TEXT,
    lane TEXT,
    kills INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    gold_per_min INTEGER,
    xp_per_min INTEGER,
    hero_damage INTEGER,
    tower_damage INTEGER,
    last_hits INTEGER,
    denies INTEGER,
    net_worth INTEGER,
    win BOOLEAN NOT NULL,
    PRIMARY KEY (player_id, match_id)
);

CREATE TABLE IF NOT EXISTS interval_stats (
    match_id TEXT NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    player_id TEXT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    interval_start_seconds INTEGER NOT NULL,
    interval_end_seconds INTEGER NOT NULL,
    metric TEXT NOT NULL,
    metric_value NUMERIC,
    item_id INTEGER REFERENCES items(item_id),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (match_id, player_id, metric, interval_start_seconds, interval_end_seconds)
);

-- Helpful indexes for query patterns
CREATE INDEX IF NOT EXISTS idx_player_matches_hero ON player_matches(hero_id);
CREATE INDEX IF NOT EXISTS idx_player_matches_team ON player_matches(team);
CREATE INDEX IF NOT EXISTS idx_interval_stats_metric ON interval_stats(metric);
CREATE INDEX IF NOT EXISTS idx_interval_stats_item ON interval_stats(item_id);
CREATE INDEX IF NOT EXISTS idx_interval_stats_player_match ON interval_stats(player_id, match_id);

-- Materialized views for analytics
DROP MATERIALIZED VIEW IF EXISTS mv_player_kda_period CASCADE;
CREATE MATERIALIZED VIEW mv_player_kda_period AS
SELECT
    pm.player_id,
    date_trunc('day', m.started_at) AS period_day,
    SUM(pm.kills) AS total_kills,
    SUM(pm.deaths) AS total_deaths,
    SUM(pm.assists) AS total_assists,
    CASE
        WHEN SUM(pm.deaths) = 0 THEN SUM(pm.kills + pm.assists)
        ELSE ROUND(SUM(pm.kills + pm.assists)::NUMERIC / NULLIF(SUM(pm.deaths), 0), 2)
    END AS kda_ratio,
    COUNT(*) AS matches_played
FROM player_matches pm
JOIN matches m ON m.match_id = pm.match_id
GROUP BY pm.player_id, period_day;

DROP MATERIALIZED VIEW IF EXISTS mv_hero_win_rates CASCADE;
CREATE MATERIALIZED VIEW mv_hero_win_rates AS
SELECT
    pm.hero_id,
    h.hero_name,
    COUNT(*) AS matches_played,
    SUM(CASE WHEN pm.win THEN 1 ELSE 0 END) AS wins,
    ROUND(SUM(CASE WHEN pm.win THEN 1 ELSE 0 END)::NUMERIC / NULLIF(COUNT(*), 0), 4) AS win_rate
FROM player_matches pm
JOIN heroes h ON h.hero_id = pm.hero_id
GROUP BY pm.hero_id, h.hero_name;

DROP MATERIALIZED VIEW IF EXISTS mv_item_timings CASCADE;
CREATE MATERIALIZED VIEW mv_item_timings AS
SELECT
    pm.hero_id,
    h.hero_name,
    ists.item_id,
    i.item_name,
    AVG(ists.interval_end_seconds) AS average_completion_seconds,
    MIN(ists.interval_end_seconds) AS fastest_completion_seconds,
    MAX(ists.interval_end_seconds) AS slowest_completion_seconds,
    COUNT(*) AS samples
FROM interval_stats ists
JOIN player_matches pm ON pm.match_id = ists.match_id AND pm.player_id = ists.player_id
JOIN heroes h ON h.hero_id = pm.hero_id
JOIN items i ON i.item_id = ists.item_id
WHERE ists.metric = 'item_timing'
GROUP BY pm.hero_id, h.hero_name, ists.item_id, i.item_name;

-- RPC helpers to allow refreshes via Supabase client
CREATE OR REPLACE FUNCTION refresh_materialized_view_mv_player_kda_period()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    REFRESH MATERIALIZED VIEW mv_player_kda_period;
END;
$$;

CREATE OR REPLACE FUNCTION refresh_materialized_view_mv_hero_win_rates()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    REFRESH MATERIALIZED VIEW mv_hero_win_rates;
END;
$$;

CREATE OR REPLACE FUNCTION refresh_materialized_view_mv_item_timings()
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    REFRESH MATERIALIZED VIEW mv_item_timings;
END;
$$;

-- Refresh all materialized views to ensure deterministic output when running the migration
REFRESH MATERIALIZED VIEW mv_player_kda_period;
REFRESH MATERIALIZED VIEW mv_hero_win_rates;
REFRESH MATERIALIZED VIEW mv_item_timings;
