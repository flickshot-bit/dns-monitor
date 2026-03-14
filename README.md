# 🌐 DNS Monitor

A real-time DNS monitoring system built with Python that tracks DNS record changes, SSL certificate expiry, and response times — with a live web dashboard.

---

## 🚀 Features

- **Real-time DNS Monitoring** — Checks A, MX, NS, and CNAME records every 60 seconds
- **Change Detection** — Instantly detects and alerts on any DNS record mutation
- **SSL Certificate Tracker** — Monitors certificate expiry with 🟢 OK / 🟡 Warning / 🔴 Critical status
- **Response Time Analysis** — Measures DNS query speed in milliseconds
- **Live Web Dashboard** — Browser-based dashboard with auto-refresh every 10 seconds
- **Historical Database** — Stores all records and changes in SQLite
- **Alert System** — Logs all changes with timestamps to alerts.log

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| DNS Queries | dnspython |
| SSL Checks | Python ssl, socket |
| Database | SQLite3 |
| Scheduling | schedule |
| Frontend | HTML, Tailwind CSS, DaisyUI |
| Charts | Chart.js |

---

## 📁 Project Structure
```
dns-monitor/
├── monitor.py          # Main controller — runs all checks
├── checker.py          # DNS record checker
├── ssl_checker.py      # SSL certificate expiry checker
├── response_time.py    # DNS response time monitor
├── alerter.py          # Alert and logging system
├── database.py         # SQLite database operations
├── app.py              # Flask web dashboard
├── config.py           # Configuration settings
├── domains.txt         # List of domains to monitor
├── static/
│   ├── script.js       # Dashboard JavaScript
│   └── style.css       # Custom styles
└── templates/
    └── index.html      # Dashboard HTML
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/dns-monitor.git
cd dns-monitor
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install dnspython schedule flask
```

### 4. Add domains to monitor
```bash
# Edit domains.txt
google.com
github.com
cloudflare.com
akamai.com
```

### 5. Run DNS Monitor
```bash
python3 monitor.py
```

### 6. Run Web Dashboard (new terminal)
```bash
python3 app.py
```

### 7. Open Dashboard
```
http://127.0.0.1:5001
```

---

## 📊 Dashboard

The live dashboard shows:
- **Total DNS checks** performed
- **Total changes** detected
- **DNS Changes Over Time** graph
- **Record Type Distribution** chart
- **Recent Changes** table with alerts
- **Latest DNS Records** table

---

## 🔒 SSL Certificate Status

| Status | Meaning |
|--------|---------|
| 🟢 OK | 30+ days remaining |
| 🟡 WARNING | Less than 30 days |
| 🔴 CRITICAL | Less than 7 days |

---

## 📈 SLI/SLO Metrics

| Metric | Target |
|--------|--------|
| DNS Resolution Success Rate | 99.9% |
| Change Detection Latency | < 60 seconds |
| Dashboard Availability | 99.9% |
| SSL Expiry Alert Lead Time | 30 days |

---

## 🎯 Production Roadmap

- [ ] Docker containerization
- [ ] PostgreSQL database upgrade
- [ ] AWS/GCP cloud deployment
- [ ] Slack/PagerDuty alert integration
- [ ] Prometheus + Grafana monitoring
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Multi-worker scaling for 100k+ domains

---

## 💡 Inspiration

Built as a hands-on project to demonstrate SRE concepts including:
- Real-time monitoring and alerting
- SLI/SLO tracking
- Certificate lifecycle management
- DNS infrastructure observability

This project directly mirrors the work done by **Akamai's Nameserver and Certificate Management SRE Team**.





MIT License — feel free to use and modify!
