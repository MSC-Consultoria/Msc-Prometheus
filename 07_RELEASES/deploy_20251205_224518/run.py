#!/usr/bin/env python
"""
Prometheus - Startup Script
Inicia o sistema completo (backend + frontend)
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def setup_environment():
    """Configurar variáveis de ambiente"""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("⚠️  Arquivo .env não encontrado!")
        print("Por favor, crie um arquivo .env com:")
        print("   OPENAI_API_KEY=seu_token_aqui")
        return False
    
    # Carregar .env
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    return True


def check_dependencies():
    """Verificar dependências"""
    print("🔍 Verificando dependências...")
    
    try:
        import flask
        import flask_cors
        import openai
        print("✅ Dependências encontradas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("\nInstale com: pip install -r requirements.txt")
        return False


def start_backend():
    """Iniciar API backend"""
    print("\n🚀 Iniciando Backend (API)...")
    
    backend_path = Path(__file__).parent / "app" / "backend" / "api.py"
    
    if not backend_path.exists():
        print(f"❌ Arquivo não encontrado: {backend_path}")
        return None
    
    # Iniciar em subprocesso
    process = subprocess.Popen(
        [sys.executable, str(backend_path)],
        cwd=str(Path(__file__).parent / "app" / "backend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print(f"✅ Backend iniciado (PID: {process.pid})")
    print("   API disponível em: http://localhost:5000")
    
    return process


def open_frontend():
    """Abrir interface frontend"""
    print("\n🌐 Abrindo Frontend...")
    
    frontend_path = Path(__file__).parent / "app" / "frontend" / "index.html"
    
    if not frontend_path.exists():
        print(f"❌ Arquivo não encontrado: {frontend_path}")
        return
    
    # Esperar um pouco para o backend iniciar
    time.sleep(2)
    
    # Abrir no navegador
    webbrowser.open(f"file://{frontend_path}")
    print(f"✅ Frontend aberto em: {frontend_path}")


def main():
    """Função principal"""
    print("=" * 50)
    print("🚀 PROMETHEUS - Agente Evolutivo")
    print("=" * 50)
    
    # Setup
    if not setup_environment():
        sys.exit(1)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Iniciar backend
    backend_process = start_backend()
    
    if not backend_process:
        sys.exit(1)
    
    # Abrir frontend
    open_frontend()
    
    print("\n" + "=" * 50)
    print("✨ Prometheus está rodando!")
    print("=" * 50)
    print("\n📊 Dashboard: http://localhost:5000")
    print("🔗 API Docs: http://localhost:5000/docs")
    print("📝 Para parar: Pressione Ctrl+C")
    print("\n" + "=" * 50)
    
    try:
        # Manter processo rodando
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n⛔ Encerrando Prometheus...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Encerrado com sucesso!")


if __name__ == "__main__":
    main()
