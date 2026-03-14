from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

def get_db_data():
    conn = sqlite3.connect('dns_monitor.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT domain, record_type, value, timestamp 
        FROM dns_records 
        ORDER BY timestamp DESC 
        LIMIT 20
    ''')
    records = cursor.fetchall()
    cursor.execute('''
        SELECT domain, record_type, old_value, new_value, detected_at 
        FROM dns_changes 
        ORDER BY detected_at DESC 
        LIMIT 10
    ''')
    changes = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM dns_records')
    total_checks = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM dns_changes')
    total_changes = cursor.fetchone()[0]
    conn.close()
    return records, changes, total_checks, total_changes

@app.route('/')
def dashboard():
    records, changes, total_checks, total_changes = get_db_data()
    return render_template('index.html',
        records=records,
        changes=changes,
        total_checks=total_checks,
        total_changes=total_changes,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route('/api/data')
def api_data():
    records, changes, total_checks, total_changes = get_db_data()
    return jsonify({
        'total_checks': total_checks,
        'total_changes': total_changes,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'records': [
            {
                'domain': r[0],
                'record_type': r[1],
                'value': r[2][:40],
                'timestamp': r[3][:16]
            } for r in records
        ],
        'changes': [
            {
                'domain': c[0],
                'record_type': c[1],
                'old_value': c[2][:30],
                'new_value': c[3][:30],
                'detected_at': c[4][:16]
            } for c in changes
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)