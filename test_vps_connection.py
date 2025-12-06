"""
Script de teste de conexão com VPS Hostinger
"""
import sys
from pathlib import Path

# Adicionar caminho do projeto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / '03_INFRAESTRUTURA'))

from app.integrations.hostinger_vps import HostingerVPS

def main():
    print("🔌 Testando Conexão com VPS Hostinger...")
    print("=" * 50)
    
    try:
        # Criar instância do cliente VPS
        vps = HostingerVPS()
        
        # Tentar conectar
        if vps.connect():
            print("\n✅ Conexão estabelecida com sucesso!")
            
            # Obter status do servidor
            print("\n📊 Status do Servidor:")
            print("-" * 50)
            status = vps.get_server_status()
            
            for key, value in status.items():
                print(f"\n{key.upper()}:")
                print(value)
            
            # Desconectar
            vps.disconnect()
            
            return 0
        else:
            print("\n❌ Falha na conexão")
            return 1
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
