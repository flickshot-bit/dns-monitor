import dns.resolver
from database import get_last_record, save_record, save_change

def check_dns(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
       
        current = sorted([str(r) for r in answers])
        current_str = ", ".join(current)
        
       
        previous = get_last_record(domain, record_type)
        
      
        save_record(domain, record_type, current_str)
        
    
        if previous and previous != current_str:
            print(f"🚨 CHANGE DETECTED: {domain} [{record_type}]")
            print(f"   Old: {previous}")
            print(f"   New: {current_str}")
            save_change(domain, record_type, previous, current_str)
            return True, previous, current_str  
            
        print(f"✅ OK: {domain} [{record_type}] = {current_str}")
        return False, None, None  
        
    except dns.resolver.NXDOMAIN:
        print(f"❌ DOMAIN NOT FOUND: {domain}")
        return False, None, None
    except dns.resolver.NoAnswer:
        print(f"⚠️  No {record_type} record for {domain}")
        return False, None, None
    except Exception as e:
        print(f"❌ ERROR checking {domain}: {e}")
        return False, None, None