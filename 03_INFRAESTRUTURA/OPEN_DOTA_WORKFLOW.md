# OpenDota → Supabase → Streamlit

Implementação base para baixar partidas, gerar arquivos XML, normalizar JSON e carregar em Supabase.

## 1. Requisitos
- Variáveis preenchidas em `.env` (copiar de `.env.example`).
- Dependências instaladas (`pip install -r 03_INFRAESTRUTURA/requirements.txt`).

## 2. Ingestão (XML + JSON)
```bash
python -m app.data.opendota.ingest --help  # via CLI improvisado
```
Ou em Python:
```python
from app.data.opendota.ingest import run_ingestion
run_ingestion(league_id=12345, output_dir="data/opendota")
```
Os XML ficam em `data/opendota/matches` e `data/opendota/players`.

## 3. Schema + carga no Supabase
```python
from app.data.opendota import SupabaseSchemaManager, SupabaseLoader
schema = SupabaseSchemaManager()
schema.apply()              # cria tabelas (requer SUPABASE_DB_URL)
loader = SupabaseLoader()   # usa SUPABASE_URL + chave
loader.load_normalized("data/opendota/normalized.json")
```

## 4. Streamlit
```bash
streamlit run 03_INFRAESTRUTURA/app/streamlit/opendota_dashboard.py
```
Use as variáveis do Supabase na sessão antes de subir o servidor (Hostinger ou local).

## 5. Colab/Juniper
Abra `notebooks/opendota_colab.ipynb` e execute as células: instalação, variáveis de ambiente, ingestão e carga no Supabase.
