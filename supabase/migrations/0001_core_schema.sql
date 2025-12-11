BEGIN;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS players (
    player_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    team_name TEXT,
    region TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS heroes (
    hero_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    primary_attribute TEXT,
    role TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category TEXT,
    description TEXT,
    cost INTEGER CHECK (cost IS NULL OR cost >= 0),
    is_consumable BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    duration_seconds INTEGER NOT NULL CHECK (duration_seconds >= 0),
    winner_team TEXT CHECK (winner_team IN ('radiant', 'dire')),
    game_mode TEXT,
    patch_version TEXT,
    region TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS player_matches (
    match_id TEXT NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    player_id TEXT NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    hero_id INTEGER REFERENCES heroes(hero_id),
    player_slot INTEGER,
    team_side TEXT CHECK (team_side IN ('radiant', 'dire')),
    is_winner BOOLEAN,
    lane TEXT,
    role TEXT,
    kills INTEGER DEFAULT 0 CHECK (kills >= 0),
    deaths INTEGER DEFAULT 0 CHECK (deaths >= 0),
    assists INTEGER DEFAULT 0 CHECK (assists >= 0),
    gold_per_minute INTEGER CHECK (gold_per_minute IS NULL OR gold_per_minute >= 0),
    xp_per_minute INTEGER CHECK (xp_per_minute IS NULL OR xp_per_minute >= 0),
    hero_damage INTEGER CHECK (hero_damage IS NULL OR hero_damage >= 0),
    tower_damage INTEGER CHECK (tower_damage IS NULL OR tower_damage >= 0),
    hero_healing INTEGER CHECK (hero_healing IS NULL OR hero_healing >= 0),
    item_timings JSONB NOT NULL DEFAULT '[]'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT player_matches_pk PRIMARY KEY (match_id, player_id),
    CONSTRAINT item_timings_is_array CHECK (jsonb_typeof(item_timings) = 'array')
);

CREATE INDEX IF NOT EXISTS idx_player_matches_hero ON player_matches(hero_id);
CREATE INDEX IF NOT EXISTS idx_player_matches_team ON player_matches(team_side);

CREATE TABLE IF NOT EXISTS interval_stats (
    match_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    interval_start_seconds INTEGER NOT NULL CHECK (interval_start_seconds >= 0),
    interval_end_seconds INTEGER NOT NULL CHECK (interval_end_seconds > interval_start_seconds),
    kills INTEGER DEFAULT 0 CHECK (kills >= 0),
    deaths INTEGER DEFAULT 0 CHECK (deaths >= 0),
    assists INTEGER DEFAULT 0 CHECK (assists >= 0),
    gold_earned INTEGER DEFAULT 0 CHECK (gold_earned >= 0),
    xp_earned INTEGER DEFAULT 0 CHECK (xp_earned >= 0),
    last_hits INTEGER DEFAULT 0 CHECK (last_hits >= 0),
    net_worth INTEGER DEFAULT 0 CHECK (net_worth >= 0),
    CONSTRAINT interval_stats_pk PRIMARY KEY (match_id, player_id, interval_start_seconds),
    CONSTRAINT fk_interval_player_match FOREIGN KEY (match_id, player_id)
        REFERENCES player_matches(match_id, player_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_interval_stats_match ON interval_stats(match_id);
CREATE INDEX IF NOT EXISTS idx_interval_stats_player ON interval_stats(player_id);

DROP MATERIALIZED VIEW IF EXISTS mv_player_kda_periods;
CREATE MATERIALIZED VIEW mv_player_kda_periods AS
SELECT
    i.player_id,
    DATE_TRUNC('day', m.started_at) AS period_start,
    SUM(i.kills) AS total_kills,
    SUM(i.deaths) AS total_deaths,
    SUM(i.assists) AS total_assists,
    ROUND((SUM(i.kills) + SUM(i.assists))::NUMERIC / NULLIF(SUM(i.deaths), 0), 3) AS kda_ratio
FROM interval_stats i
JOIN matches m ON m.match_id = i.match_id
GROUP BY i.player_id, DATE_TRUNC('day', m.started_at);

CREATE UNIQUE INDEX idx_mv_player_kda_periods ON mv_player_kda_periods (player_id, period_start);

DROP MATERIALIZED VIEW IF EXISTS mv_hero_win_rates;
CREATE MATERIALIZED VIEW mv_hero_win_rates AS
SELECT
    pm.hero_id,
    h.name AS hero_name,
    COUNT(*) AS games_played,
    SUM(CASE WHEN pm.is_winner THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN NOT pm.is_winner THEN 1 ELSE 0 END) AS losses,
    ROUND(SUM(CASE WHEN pm.is_winner THEN 1 ELSE 0 END)::NUMERIC / NULLIF(COUNT(*), 0), 4) AS win_rate
FROM player_matches pm
LEFT JOIN heroes h ON h.hero_id = pm.hero_id
GROUP BY pm.hero_id, h.name;

CREATE UNIQUE INDEX idx_mv_hero_win_rates ON mv_hero_win_rates (hero_id);

DROP MATERIALIZED VIEW IF EXISTS mv_item_timings;
CREATE MATERIALIZED VIEW mv_item_timings AS
SELECT
    entry.item_id,
    i.name AS item_name,
    pm.hero_id,
    h.name AS hero_name,
    COUNT(*) AS purchase_count,
    AVG(entry.time_seconds)::NUMERIC(12, 2) AS avg_purchase_time_seconds,
    MIN(entry.time_seconds) AS fastest_purchase_seconds,
    MAX(entry.time_seconds) AS slowest_purchase_seconds
FROM player_matches pm
CROSS JOIN LATERAL jsonb_to_recordset(pm.item_timings) AS entry(item_id INT, time_seconds INT)
LEFT JOIN items i ON i.item_id = entry.item_id
LEFT JOIN heroes h ON h.hero_id = pm.hero_id
GROUP BY entry.item_id, i.name, pm.hero_id, h.name;

CREATE INDEX idx_mv_item_timings_item ON mv_item_timings(item_id);
CREATE INDEX idx_mv_item_timings_hero ON mv_item_timings(hero_id);

COMMIT;
