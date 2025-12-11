# OpenDota + Supabase + Streamlit Deployment Guide

This guide describes how to run the OpenDota ETL and the Streamlit dashboard behind nginx on the Hostinger VPS.

## Prerequisites
- Docker and Docker Compose installed on the VPS
- Supabase project with the SQL schema from `opendota_supabase/schema.sql` applied (SQL editor or `psql`)
- `.env` file based on `.env.example`

## 1) Prepare environment variables
Copy the sample file and fill in your values:

```bash
cp .env.example .env
# edit the file with your OpenDota and Supabase credentials
```

At minimum set:
- `OPENDOTA_PLAYER_IDS` – comma-separated player IDs to sync
- `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` – used by the ETL
- `SUPABASE_ANON_KEY` – used by the Streamlit dashboard

## 2) Build and run with Docker Compose
The compose stack lives in `opendota_supabase/docker-compose.yml` and builds the Streamlit image, then proxies it through nginx.

```bash
cd /path/to/Msc-Prometheus/opendota_supabase
sudo docker compose up -d --build
```

The stack exposes port `80` for nginx. Health checks are available at `http://<server>/healthz` (served directly by nginx).

## 3) Load the Supabase schema
Apply `opendota_supabase/schema.sql` in the Supabase SQL editor to create `dota_players` and `dota_matches`.

## 4) Run the ETL
The ETL pulls recent matches and player profiles for the configured player IDs and upserts them into Supabase.

- Run locally (with your virtualenv activated):
  ```bash
  python -m opendota_supabase.etl
  ```
- Run inside the container:
  ```bash
  cd /path/to/Msc-Prometheus/opendota_supabase
  sudo docker compose run --rm streamlit python etl.py
  ```

Schedule the ETL with cron/systemd if you want automatic refreshes (e.g., hourly).

## 5) Optional systemd units
If you prefer systemd over Docker Compose, create `/etc/systemd/system/opendota-streamlit.service`:

```
[Unit]
Description=OpenDota Streamlit dashboard
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/Msc-Prometheus
EnvironmentFile=/path/to/Msc-Prometheus/.env
ExecStart=/usr/bin/streamlit run /path/to/Msc-Prometheus/opendota_supabase/streamlit_app.py --server.address=0.0.0.0 --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Pair it with nginx (same `opendota_supabase/nginx.conf`, update the upstream to `http://127.0.0.1:8501`).

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now opendota-streamlit.service
```

## Notes
- Health check endpoint: `http://<server>/healthz` returns `200 ok` for uptime monitoring.
- CI linting/formatting runs via `.github/workflows/ci.yml` (ruff + black) to keep the Python codebase tidy.
