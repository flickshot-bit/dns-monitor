import dns.resolver
import time

def check_response_time(domain):
    try:
        start = time.time()
        dns.resolver.resolve(domain, 'A')
        end = time.time()
        
        ms = round((end - start) * 1000, 2)
        
        if ms < 50:
            status = "🟢 FAST"
        elif ms < 100:
            status = "🟡 OK"
        else:
            status = "🔴 SLOW"
            
        print(f"{status}: {domain} resolved in {ms}ms")
        return ms
        
    except Exception as e:
        print(f"❌ ERROR: {domain} — {e}")
        return None