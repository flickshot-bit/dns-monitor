
from datetime import datetime

def send_alert(domain, record_type, old_val, new_val):
    message = f"""
    ============================
    🚨 DNS CHANGE ALERT
    ============================
    Domain      : {domain}
    Record Type : {record_type}
    Old Value   : {old_val}
    New Value   : {new_val}
    Time        : {datetime.now()}
    ============================
    """
    print(message)
    
    with open("alerts.log", "a") as f:
        f.write(message + "\n")