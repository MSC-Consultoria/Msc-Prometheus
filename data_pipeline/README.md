# Data Pipeline Utilities

## OpenDota ETL

The OpenDota tournament ingestor lives in `data_pipeline/opendota_ingest.py` and offers a CLI for collecting match and player data.

### Environment
- `OPENDOTA_BASE_URL` (optional): overrides the API base URL.
- `OPENDOTA_API_KEY` (optional): premium API key for elevated rate limits.

### Installation
Install runtime dependencies (requests, pandas, pyarrow) from the shared requirements file:

```bash
pip install -r 03_INFRAESTRUTURA/requirements.txt
```

### CLI usage

```bash
python -m data_pipeline.opendota_ingest --tournament <league_id> --out data/raw_xml \
  --base-url https://api.opendota.com/api --api-key "$OPENDOTA_API_KEY" --log-level INFO
```

Use `--max-matches` to limit ingestion during testing.
