"""
Script auxiliar para executar o deploy no VPS
Chamado pelo deploy_vps.ps1
"""
import sys
import os
from pathlib import Path

# Adicionar caminho do projeto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / '03_INFRAESTRUTURA'))

from app.integrations.hostinger_vps import HostingerVPS

def main():
    if len(sys.argv) < 2:
        print("❌ Erro: Diretório de deploy não especificado")
        sys.exit(1)
        
    deploy_dir = sys.argv[1]
    print(f"🚀 Iniciando deploy a partir de: {deploy_dir}")
    
    vps = HostingerVPS()
    if vps.connect():
        print('✅ Conectado ao VPS!')
        
        # Upload dos arquivos
        local_path = deploy_dir
        remote_path = '/var/www/prometheus'
        
        print(f'📦 Uploading from {local_path} to {remote_path}...')
        
        # Criar diretório remoto
        vps.execute_command(f'mkdir -p {remote_path}')
        
        # Upload recursivo via SFTP
        def upload_dir(local, remote):
            # Criar diretório remoto se não existir
            try:
                vps.sftp.mkdir(remote)
            except:
                pass # Provavelmente já existe
                
            for item in os.listdir(local):
                l_item = os.path.join(local, item)
                # Normalizar caminho remoto (usar / sempre)
                r_item = remote + '/' + item
                r_item = r_item.replace('\\', '/')
                
                if os.path.isfile(l_item):
                    print(f"  📄 Uploading: {item}")
                    vps.sftp.put(l_item, r_item)
                elif os.path.isdir(l_item):
                    print(f"  wd Folder: {item}")
                    upload_dir(l_item, r_item)
                    
        # Upload
        try:
            upload_dir(local_path, remote_path)
            print('✅ Upload concluído!')
            
            # Executar configuração
            vps.deploy_prometheus()
            
        except Exception as e:
            print(f"❌ Erro durante upload/deploy: {e}")
            import traceback
            traceback.print_exc()
        finally:
            vps.disconnect()
    else:
        print('❌ Falha na conexão')
        sys.exit(1)

if __name__ == "__main__":
    main()
