from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / '03_INFRAESTRUTURA'))
from app.integrations.hostinger_vps import HostingerVPS

print("Starting check...")
vps = HostingerVPS()
if vps.connect():
    print("Checking /var/www/prometheus content...")
    res = vps.execute_command("ls -la /var/www/prometheus")
    print(res['stdout'])
    
    print("Checking main.py...")
    res = vps.execute_command("ls -la /var/www/prometheus/main.py")
    print(res['stdout'])

    print("Checking api.py...")
    res = vps.execute_command("ls -la /var/www/prometheus/app/backend/api.py")
    print(res['stdout'])

    print("Checking nginx status...")
    res = vps.execute_command("systemctl status nginx")
    print(res['stdout'])
    
    print("Checking prometheus service...")
    res = vps.execute_command("systemctl status prometheus")
    print(res['stdout'])
    
    print("Checking service logs...")
    res = vps.execute_command("journalctl -u prometheus -n 20 --no-pager")
    print(res['stdout'])
    
    print("Checking API response...")
    res = vps.execute_command("curl -v http://127.0.0.1:5000/api/health")
    print(res['stdout'])
    print(res['stderr'])
    
    vps.disconnect()
else:
    print("Failed to connect")
