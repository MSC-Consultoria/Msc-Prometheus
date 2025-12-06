from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / '03_INFRAESTRUTURA'))
from app.integrations.hostinger_vps import HostingerVPS

vps = HostingerVPS()
if vps.connect():
    print("Checking dashboard.html content...")
    res = vps.execute_command("grep 'Família' /var/www/prometheus/app/frontend/dashboard.html")
    print(res['stdout'])
    
    vps.disconnect()
else:
    print("Failed to connect")
