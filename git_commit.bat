@echo off
cd /d "c:\Users\Festeja\Downloads\Prometheus"

echo === Prometheus Git Setup ===
echo.

REM Remover .git incorreto
if exist "03_INFRAESTRUTURA\.git" (
    echo Removendo repositorio Git incorreto...
    rmdir /s /q "03_INFRAESTRUTURA\.git"
)

REM Adicionar arquivos
echo Adicionando arquivos ao Git...
git add --all

echo.
echo Arquivos staged:
git diff --cached --name-status | find /c /v ""

echo.
echo Fazendo commit...
git commit -m "Initial commit: Prometheus AI Agent System - Backend Flask API with 20+ endpoints - Frontend dashboard - Multi-LLM support - GitHub and N8N integrations - Documentation and issues"

echo.
echo === Status Final ===
git log --oneline -1
git status

echo.
echo Proximos passos:
echo 1. Criar repo no GitHub: https://github.com/new
echo 2. Conectar: git remote add origin https://github.com/seu-usuario/prometheus-ai-agent.git
echo 3. Push: git branch -M main; git push -u origin main

pause
