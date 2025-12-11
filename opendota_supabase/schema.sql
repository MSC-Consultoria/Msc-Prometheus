-- Supabase schema for OpenDota ETL
CREATE TABLE IF NOT EXISTS public.dota_players (
    player_id TEXT PRIMARY KEY,
    personaname TEXT,
    name TEXT,
    mmr INTEGER,
    rank_tier INTEGER,
    profile_url TEXT,
    avatar TEXT,
    last_login TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.dota_matches (
    match_id BIGINT PRIMARY KEY,
    player_id TEXT REFERENCES public.dota_players(player_id),
    hero_id INTEGER,
    kills INTEGER,
    deaths INTEGER,
    assists INTEGER,
    duration INTEGER,
    player_slot INTEGER,
    radiant_win BOOLEAN,
    start_time TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_dota_matches_start_time ON public.dota_matches (start_time DESC);
