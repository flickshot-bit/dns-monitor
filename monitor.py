import schedule
import time
from database import init_db
from checker import check_dns
from alerter import send_alert
from ssl_checker import check_ssl
from response_time import check_response_time
from config import CHECK_INTERVAL, CHECK_TYPES
from datetime import datetime

def load_domains():
    with open("domains.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_checks():
    domains = load_domains()
    print(f"\n⏰ Check started at {datetime.now()}")
    print(f"📋 Checking {len(domains)} domains...\n")

    changes_found = 0
    for domain in domains:
        for record_type in CHECK_TYPES:
            changed, old, new = check_dns(domain, record_type)
            if changed:
                send_alert(domain, record_type, old, new)
                changes_found += 1

    print(f"\n📊 Summary: {changes_found} changes detected")
    print("-" * 40)

    print("\n🔒 SSL Certificate Check:")
    print("-" * 40)
    for domain in domains:
        check_ssl(domain)

    print("\n⚡ Response Time Check:")
    print("-" * 40)
    for domain in domains:
        check_response_time(domain)

def main():
    print("🚀 DNS Monitor Starting...")
    init_db()

    run_checks()

    schedule.every(CHECK_INTERVAL).seconds.do(run_checks)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()