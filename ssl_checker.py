import ssl
import socket
from datetime import datetime
from database import save_record

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain
        )
        conn.settimeout(5.0)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        conn.close()

    
        expiry_str = cert['notAfter']
        expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry_date - datetime.now()).days

    
        if days_left <= 7:
            status = "🔴 CRITICAL"
        elif days_left <= 30:
            status = "🟡 WARNING"
        else:
            status = "🟢 OK"

        print(f"{status}: {domain} | Expires in {days_left} days | {expiry_date.strftime('%d-%m-%Y')}")
        return days_left

    except Exception as e:
        print(f"❌ ERROR: {domain} SSL check failed — {e}")
        return None