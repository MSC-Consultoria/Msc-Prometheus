# Status do Deploy - Hostinger VPS

**Data:** 06/12/2025
**Status:** ✅ ONLINE
**URL:** http://72.62.9.90

## Componentes
- **Frontend:** Nginx servindo arquivos estáticos em `/var/www/prometheus/app/frontend`
- **Backend:** Flask API rodando via Systemd em `http://127.0.0.1:5000` (proxied por Nginx em `/api`)
- **Banco de Dados:** SQLite (local)

## Verificação
- **Nginx:** Active (running)
- **Prometheus Service:** Active (running)
- **API Health:** OK (`/api/health` retornou 200)

## Próximos Passos
1. Configurar HTTPS (SSL)
2. Configurar variáveis de ambiente (GITHUB_TOKEN, N8N_KEY) no arquivo `.env` no servidor.
3. Configurar CI/CD automático via GitHub Actions (opcional).
