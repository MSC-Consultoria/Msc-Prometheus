# Script para inicializar Git e fazer primeiro commit
Set-Location "c:\Users\Festeja\Downloads\Prometheus"

Write-Host "=== Prometheus Git Setup ===" -ForegroundColor Cyan
Write-Host ""

# Remover git incorreto se existir
if (Test-Path "03_INFRAESTRUTURA\.git") {
    Write-Host "Removendo repositório Git incorreto..." -ForegroundColor Yellow
    Remove-Item -Force -Recurse "03_INFRAESTRUTURA\.git"
}

# Verificar se já existe repositório
if (Test-Path ".git") {
    Write-Host "Repositório Git já existe. Pulando inicialização." -ForegroundColor Green
} else {
    Write-Host "Inicializando repositório Git..." -ForegroundColor Cyan
    git init
}

# Configurar usuário
Write-Host "Configurando usuário Git..." -ForegroundColor Cyan
git config user.name "Festeja"
git config user.email "festeja@prometheus.local"

# Adicionar arquivos
Write-Host "Adicionando arquivos ao staging..." -ForegroundColor Cyan
git add -A

# Mostrar status
Write-Host ""
Write-Host "Status do repositório:" -ForegroundColor Cyan
git status --short | Select-Object -First 50

# Contar arquivos
$fileCount = (git ls-files | Measure-Object -Line).Lines
Write-Host ""
Write-Host "Total de arquivos adicionados: $fileCount" -ForegroundColor Green

# Fazer commit
Write-Host ""
Write-Host "Fazendo commit inicial..." -ForegroundColor Cyan
git commit -m "Initial commit: Prometheus AI Agent System

- Backend Flask API with 20+ endpoints
- Frontend dashboard with 7 sections  
- Multi-LLM support (OpenAI, Claude, Gemini, DeepSeek, OpenRouter)
- GitHub and N8N integrations
- Comprehensive documentation (1650+ lines)
- 10 detailed GitHub issues created
- Project evaluation completed (54/100 score)
- Total files: 150+"

Write-Host ""
Write-Host "=== Commit completo! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Criar repositório no GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Cyan
Write-Host "2. Conectar com o repositório remoto:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/seu-usuario/prometheus-ai-agent.git" -ForegroundColor Cyan
Write-Host "3. Fazer push:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "Log do commit:" -ForegroundColor Yellow
git log --oneline -1
