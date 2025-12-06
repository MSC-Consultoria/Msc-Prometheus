# Script de Deploy para VPS Hostinger
# Automatiza o processo de deploy do Prometheus

Write-Host "🚀 Prometheus Deploy Script" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar se tem alterações para commitar
Write-Host "📋 Verificando alterações locais..." -ForegroundColor Yellow
# $status = git status --porcelain
# if ($status) {
#     Write-Host "⚠️ Há alterações não commitadas!" -ForegroundColor Red
#     Write-Host "Pulando verificação de git para deploy automático..." -ForegroundColor Yellow
# }

# 2. Criar pacote para deploy
Write-Host ""
Write-Host "📦 Criando pacote de deploy..." -ForegroundColor Yellow

$deployDir = "07_RELEASES\deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $deployDir -Force | Out-Null

# Copiar arquivos essenciais
Copy-Item "03_INFRAESTRUTURA\*" -Destination $deployDir -Recurse -Force
# requirements.txt e .env.example já estão dentro de 03_INFRAESTRUTURA

Write-Host "✅ Pacote criado em: $deployDir" -ForegroundColor Green

# 3. Conectar ao VPS e fazer deploy
Write-Host ""
Write-Host "🌐 Conectando ao VPS Hostinger..." -ForegroundColor Yellow
Write-Host "Host: 72.62.9.90" -ForegroundColor Cyan

# Usar Python para fazer o deploy
# Chamando script externo para evitar problemas de encoding no PowerShell
$pythonPath = "C:/Users/Festeja/Downloads/Prometheus/.venv/Scripts/python.exe"
if (-not (Test-Path $pythonPath)) {
    $pythonPath = "python"
}

& $pythonPath deploy_runner.py "$deployDir"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deploy concluído com sucesso!" -ForegroundColor Green
    Write-Host "🌍 Acesse: http://72.62.9.90" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Erro no deploy" -ForegroundColor Red
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
