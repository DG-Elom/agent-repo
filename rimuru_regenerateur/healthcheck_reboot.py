import os
import time
import requests

SERVICE_URL = "http://localhost:6789"  # URL à surveiller
REBOOT_COMMAND = "systemctl restart mageai"  # Commande de redémarrage
LOGFILE = "rimuru_health.log"

def check_service():
    try:
        r = requests.get(SERVICE_URL, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

def reboot_service():
    os.system(REBOOT_COMMAND)
    with open(LOGFILE, "a") as f:
        f.write(f"[{time.ctime()}] Reboot triggered\n")

if __name__ == "__main__":
    if not check_service():
        reboot_service()