import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("dns_monitor.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns_records (
            id INTEGER PRIMARY KEY,
            domain TEXT,
            record_type TEXT,
            value TEXT,
            timestamp DATETIME
        )
    ''')
    

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns_changes (
            id INTEGER PRIMARY KEY,
            domain TEXT,
            record_type TEXT,
            old_value TEXT,
            new_value TEXT,
            detected_at DATETIME
        )
    ''')
    
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uptime_log (
            id INTEGER PRIMARY KEY,
            domain TEXT,
            status TEXT,   -- 'UP' or 'DOWN'
            checked_at DATETIME
        )
    ''')
    
    conn.commit()
    conn.close()

def save_record(domain, record_type, value):
    conn = sqlite3.connect("dns_monitor.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dns_records (domain, record_type, value, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (domain, record_type, value, datetime.now()))
    conn.commit()
    conn.close()

def save_change(domain, record_type, old_val, new_val):
    conn = sqlite3.connect("dns_monitor.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dns_changes 
        (domain, record_type, old_value, new_value, detected_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (domain, record_type, old_val, new_val, datetime.now()))
    conn.commit()
    conn.close()

def get_last_record(domain, record_type):
    conn = sqlite3.connect("dns_monitor.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT value FROM dns_records 
        WHERE domain=? AND record_type=?
        ORDER BY timestamp DESC LIMIT 1
    ''', (domain, record_type))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None