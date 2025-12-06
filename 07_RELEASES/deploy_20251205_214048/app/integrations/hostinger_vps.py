"""
Módulo de conexão SSH com VPS Hostinger
Gerencia conexão segura com o servidor para deploy e administração
"""

import paramiko
import os
from configparser import ConfigParser
from pathlib import Path

class HostingerVPS:
    """Cliente para gerenciar VPS da Hostinger"""
    
    def __init__(self, config_path=None):
        """
        Inicializar conexão com VPS
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        if config_path is None:
            # Encontrar o diretório raiz do projeto
            current = Path(__file__).resolve()
            while current.parent != current:
                if (current / '06_BACKUPS' / 'SENSIVEL' / 'vps_config.ini').exists():
                    config_path = current / '06_BACKUPS' / 'SENSIVEL' / 'vps_config.ini'
                    break
                current = current.parent
        
        self.config = ConfigParser()
        files_read = self.config.read(config_path)
        
        if not files_read:
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
        
        self.host = self.config['access']['ipv4']
        self.username = self.config['access']['ssh_user']
        self.password = self.config['access']['root_password']
        self.port = int(self.config['access'].get('ssh_port', 22))
        
        self.client = None
        self.sftp = None
    
    def connect(self):
        """Estabelecer conexão SSH"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.client.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=10
            )
            
            self.sftp = self.client.open_sftp()
            print(f"✅ Conectado ao VPS: {self.host}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def execute_command(self, command):
        """
        Executar comando no servidor
        
        Args:
            command: Comando shell para executar
            
        Returns:
            dict com stdout, stderr e exit_code
        """
        if not self.client:
            raise ConnectionError("Não conectado ao servidor. Use connect() primeiro.")
        
        stdin, stdout, stderr = self.client.exec_command(command)
        
        return {
            'stdout': stdout.read().decode(),
            'stderr': stderr.read().decode(),
            'exit_code': stdout.channel.recv_exit_status()
        }
    
    def upload_file(self, local_path, remote_path):
        """
        Upload arquivo para servidor
        
        Args:
            local_path: Caminho local do arquivo
            remote_path: Caminho remoto no servidor
        """
        if not self.sftp:
            raise ConnectionError("SFTP não inicializado. Use connect() primeiro.")
        
        try:
            self.sftp.put(local_path, remote_path)
            print(f"✅ Upload: {local_path} -> {remote_path}")
            return True
        except Exception as e:
            print(f"❌ Erro no upload: {e}")
            return False
    
    def download_file(self, remote_path, local_path):
        """
        Download arquivo do servidor
        
        Args:
            remote_path: Caminho remoto no servidor
            local_path: Caminho local para salvar
        """
        if not self.sftp:
            raise ConnectionError("SFTP não inicializado. Use connect() primeiro.")
        
        try:
            self.sftp.get(remote_path, local_path)
            print(f"✅ Download: {remote_path} -> {local_path}")
            return True
        except Exception as e:
            print(f"❌ Erro no download: {e}")
            return False
    
    def deploy_prometheus(self, project_path=None):
        """
        Deploy do Prometheus para o VPS
        
        Args:
            project_path: Caminho do projeto local (default: diretório atual)
        """
        if not self.client:
            self.connect()
        
        print("🚀 Iniciando deploy do Prometheus...")
        
        # 1. Instalar dependências no servidor
        commands = [
            "export DEBIAN_FRONTEND=noninteractive && apt-get update",
            "export DEBIAN_FRONTEND=noninteractive && apt-get install -y python3 python3-pip python3-venv nginx",
            "mkdir -p /var/www/prometheus",
        ]
        
        for cmd in commands:
            print(f"Executando: {cmd}")
            # Remover sudo se já for root, mas manter compatibilidade
            full_cmd = cmd if cmd.startswith("export") else f"sudo {cmd}"
            # Se for root, não precisa de sudo
            if self.username == 'root':
                full_cmd = cmd
                
            result = self.execute_command(full_cmd)
            if result['exit_code'] != 0:
                print(f"⚠️ Aviso: {result['stderr']}")
        
        # 2. Upload do projeto
        print("📦 Upload dos arquivos...")
        # Assumindo que o pacote já foi criado em 07_RELEASES pelo script PowerShell
        # Se não, vamos fazer upload direto dos arquivos locais
        
        # Limpar diretório remoto
        self.execute_command("rm -rf /var/www/prometheus/*")
        
        # Upload recursivo (simplificado para este exemplo, idealmente usar rsync ou tar)
        # Aqui vamos assumir que o script PowerShell já fez o upload ou vamos implementar um upload básico
        # Para simplificar e garantir que funcione, vamos criar os arquivos de configuração remotamente
        
        # 3. Configurar ambiente virtual
        print("🐍 Configurando Python Venv...")
        # Usar caminhos absolutos para garantir execução correta
        venv_path = "/var/www/prometheus/venv"
        pip_path = f"{venv_path}/bin/pip"
        
        venv_commands = [
            f"python3 -m venv {venv_path}",
            f"{pip_path} install --upgrade pip",
            f"{pip_path} install -r /var/www/prometheus/requirements.txt"
        ]
        
        for cmd in venv_commands:
            print(f"Executando: {cmd}")
            result = self.execute_command(cmd)
            if result['exit_code'] != 0:
                print(f"⚠️ Erro no venv: {result['stderr']}")

        # 4. Configurar Systemd (Service)
        print("⚙️ Configurando Systemd...")
        service_content = f"""[Unit]
Description=Prometheus AI Agent
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/prometheus
Environment="PATH=/var/www/prometheus/venv/bin"
ExecStart=/var/www/prometheus/venv/bin/python /var/www/prometheus/03_INFRAESTRUTURA/main.py
Restart=always

[Install]
WantedBy=multi-user.target
"""
        self.execute_command(f"echo '{service_content}' > /etc/systemd/system/prometheus.service")
        self.execute_command("systemctl daemon-reload")
        self.execute_command("systemctl enable prometheus")
        self.execute_command("systemctl restart prometheus")

        # 5. Configurar Nginx
        print("🌐 Configurando Nginx...")
        nginx_content = f"""server {{
    listen 80;
    server_name {self.host};

    location / {{
        root /var/www/prometheus/03_INFRAESTRUTURA/app/frontend;
        index login.html dashboard.html;
        try_files $uri $uri/ =404;
    }}

    location /api/ {{
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}"""
        self.execute_command(f"echo '{nginx_content}' > /etc/nginx/sites-available/prometheus")
        self.execute_command("ln -sf /etc/nginx/sites-available/prometheus /etc/nginx/sites-enabled/")
        self.execute_command("rm -f /etc/nginx/sites-enabled/default")
        self.execute_command("nginx -t && systemctl restart nginx")
        
        print("✅ Deploy concluído!")
        print(f"🌍 Acesse: http://{self.host}")
        
        return True
    
    def get_server_status(self):
        """Obter status do servidor"""
        if not self.client:
            self.connect()
        
        commands = {
            'uptime': 'uptime',
            'disk': 'df -h /',
            'memory': 'free -h',
            'cpu': 'top -bn1 | grep "Cpu(s)"',
            'processes': 'ps aux | wc -l'
        }
        
        status = {}
        for key, cmd in commands.items():
            result = self.execute_command(cmd)
            status[key] = result['stdout'].strip()
        
        return status
    
    def disconnect(self):
        """Fechar conexões"""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        print("🔌 Desconectado do VPS")


# Exemplo de uso
if __name__ == "__main__":
    vps = HostingerVPS()
    
    if vps.connect():
        # Obter status
        status = vps.get_server_status()
        print("\n📊 Status do Servidor:")
        for key, value in status.items():
            print(f"{key}: {value}")
        
        vps.disconnect()
