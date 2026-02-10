# 🖥️ Infrastructure Monitoring System

<p align="center">
  <strong>Enterprise-Grade Server Monitoring with Prometheus & Grafana</strong><br>
  <em>Real-time KPIs • Dynamic Metrics • Automated Alerts</em>
</p>

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [System Architecture](#-system-architecture)
3. [Components](#-components)
4. [Data Flow](#-data-flow)
5. [KPI Metrics & Formulas](#-kpi-metrics--formulas)
6. [File Structure](#-file-structure)
7. [Installation Guide](#-installation-guide)
8. [Grafana Setup](#-grafana-setup)
9. [Configuration](#-configuration)
10. [Alert Rules](#-alert-rules)
11. [API Endpoints](#-api-endpoints)
12. [Troubleshooting](#-troubleshooting)
13. [Screenshots](#-screenshots)

---

## 📖 Overview

This Infrastructure Monitoring System provides comprehensive server monitoring capabilities for RHEL 9 environments. It combines industry-standard tools (Prometheus, Grafana) with custom Python exporters to deliver real-time visibility into system health, energy efficiency, and business KPIs.

### Key Features

| Feature | Description |
|---------|-------------|
| **Dynamic Metrics** | Edit JSON file → See changes in Grafana within 30 seconds |
| **Real-time Monitoring** | 15-second scrape intervals for near real-time data |
| **Automated Alerts** | 6 pre-configured alert rules for proactive monitoring |
| **Energy Tracking** | Calculate and visualize energy savings and CO2 reduction |
| **Service Monitoring** | Track status of critical systemd services |
| **100% Open Source** | No licensing fees, no vendor lock-in |

### Server Information

| Parameter | Value |
|-----------|-------|
| Server IP | `172.31.3.177` |
| Operating System | RHEL 9 |
| Author | Aykhan |
| Version | 3.1 |

---

## 🏗️ System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         INFRASTRUCTURE MONITORING SYSTEM                            │
│                              Server: 172.31.3.177                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌─────────────┐
│   DATA SOURCES   │    │    EXPORTERS     │    │   PROMETHEUS     │    │   GRAFANA   │
│                  │    │                  │    │                  │    │             │
│ ┌──────────────┐ │    │ ┌──────────────┐ │    │                  │    │             │
│ │ metrics.json │─┼───►│ │   Metrics    │─┼───►│                  │    │  ┌───────┐  │
│ │   (KPIs)     │ │    │ │   Exporter   │ │    │   Time Series    │    │  │Gauges │  │
│ └──────────────┘ │    │ │  Port: 9101  │ │    │    Database      │───►│  │Graphs │  │
│                  │    │ └──────────────┘ │    │                  │    │  │Charts │  │
│ ┌──────────────┐ │    │                  │    │  Scrapes every   │    │  └───────┘  │
│ │   System     │─┼───►│ ┌──────────────┐ │    │   15 seconds     │    │             │
│ │   Metrics    │ │    │ │    Node      │─┼───►│                  │    │  Dashboard  │
│ └──────────────┘ │    │ │   Exporter   │ │    │   Evaluates      │    │  Port: 3000 │
│                  │    │ │  Port: 9100  │ │    │   Alert Rules    │    │             │
│ ┌──────────────┐ │    │ └──────────────┘ │    │                  │    │             │
│ │   Service    │─┼───►│                  │    │   Port: 9090     │    │             │
│ │   Status     │ │    │ ┌──────────────┐ │    │                  │    │             │
│ └──────────────┘ │    │ │   Service    │─┼───►│                  │    │             │
│                  │    │ │   Checker    │ │    │                  │    │             │
│                  │    │ │  Port: 9102  │ │    │                  │    │             │
│                  │    │ └──────────────┘ │    │                  │    │             │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └─────────────┘
```

### Component Communication

```
                                    HTTP GET /metrics
┌─────────────────┐                 every 15 seconds                 ┌─────────────────┐
│                 │ ◄──────────────────────────────────────────────► │                 │
│   PROMETHEUS    │                                                  │    EXPORTERS    │
│   Port: 9090    │                                                  │  9100/9101/9102 │
│                 │                 HTTP Queries                     │                 │
└────────┬────────┘ ◄──────────────────────────────────────────────► └─────────────────┘
         │
         │ PromQL Queries
         ▼
┌─────────────────┐
│     GRAFANA     │
│   Port: 3000    │
│   Dashboards    │
└─────────────────┘
```

---

## 🔧 Components

### 1. Prometheus (Port 9090)

**Purpose:** Time-series database for metrics collection and alerting

| Feature | Description |
|---------|-------------|
| Scrape Interval | 15 seconds |
| Evaluation Interval | 15 seconds |
| Data Retention | Default 15 days |
| Query Language | PromQL |

**URLs:**
- Main UI: `http://172.31.3.177:9090`
- Targets: `http://172.31.3.177:9090/targets`
- Alerts: `http://172.31.3.177:9090/alerts`
- API: `http://172.31.3.177:9090/api/v1/`

### 2. Grafana (Port 3000)

**Purpose:** Visualization and dashboarding platform

| Feature | Description |
|---------|-------------|
| Dashboard | Pre-configured with KPI gauges |
| Data Source | Prometheus |
| Refresh Rate | 30 seconds |
| Authentication | admin / admin (default) |

**Dashboard Panels:**
- Energy Reduction Gauge
- Cost Savings Display
- CO2 Reduction Gauge
- Security Threats Counter
- Server Status Overview
- Service Status Grid
- CPU/Memory Time Series

### 3. Metrics Exporter (Port 9101)

**Purpose:** Reads KPI data from JSON and exposes to Prometheus

| Parameter | Value |
|-----------|-------|
| Port | 9101 |
| Reload Interval | 10 seconds |
| Data Source | HTTP endpoint (metrics.json) |
| Language | Python 3 |

**Exposed Metrics:**
```
achievement_energy_reduction_percent
achievement_cost_savings_azn
achievement_co2_reduction_kg
achievement_security_threats_detected
achievement_avg_cpu_percent
achievement_servers_online
```

### 4. Service Checker (Port 9102)

**Purpose:** Monitors systemd service status

| Parameter | Value |
|-----------|-------|
| Port | 9102 |
| Check Interval | 30 seconds |
| Language | Python 3 |

**Monitored Services:**
- prometheus
- grafana-server
- node_exporter
- nginx / httpd
- postgresql / mariadb / redis
- sshd / firewalld / crond

**Exposed Metrics:**
```
service_status{service="name"}     # 1=running, 0=stopped
services_total                      # Total monitored
services_running                    # Currently running
```

### 5. Node Exporter (Port 9100)

**Purpose:** System metrics (CPU, Memory, Disk, Network)

| Metric Category | Examples |
|----------------|----------|
| CPU | `node_cpu_seconds_total` |
| Memory | `node_memory_MemAvailable_bytes` |
| Disk | `node_filesystem_avail_bytes` |
| Network | `node_network_receive_bytes_total` |

### 6. Mock Metrics Server (Port 9200)

**Purpose:** Simulates dynamic KPI data for testing

| Parameter | Value |
|-----------|-------|
| Port | 9200 |
| Endpoint | `/metrics-json` |
| Language | Node.js |

---

## 🔄 Data Flow

### Dynamic Metrics Update Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DYNAMIC METRICS FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

    STEP 1                    STEP 2                    STEP 3                STEP 4
  ┌─────────┐              ┌─────────────┐           ┌───────────┐         ┌─────────┐
  │  Edit   │   10 sec     │   Metrics   │  15 sec   │Prometheus │ Instant │ Grafana │
  │  JSON   │ ──────────►  │  Exporter   │ ───────►  │  Scrapes  │ ──────► │ Updates │
  │  File   │   Reads      │  Converts   │  Pulls    │  Stores   │ Query   │ Display │
  └─────────┘              └─────────────┘           └───────────┘         └─────────┘

  User changes              Python script            Time-series          Dashboard
  metrics.json              reads file and           database stores      shows new
  values                    exposes metrics          new values           values

                        TOTAL TIME: ~30 SECONDS
```

### Alert Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Metrics    │     │  Prometheus  │     │    Alert     │     │ Notification │
│   Scraped    │────►│   Evaluates  │────►│   Fires      │────►│    Sent      │
│              │     │    Rules     │     │              │     │  (Optional)  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 📊 KPI Metrics & Formulas

### Energy Efficiency Metrics

The system calculates energy efficiency based on server load and baseline consumption.

#### Dashboard Preview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 KPI DASHBOARD                                        │
├───────────────┬───────────────┬───────────────┬───────────────┬─────────────────────┤
│    ENERGY     │  COST SAVINGS │ CO2 REDUCTION │   SECURITY    │      SERVERS        │
├───────────────┼───────────────┼───────────────┼───────────────┼─────────────────────┤
│ Reduction %   │ Monthly (AZN) │ Monthly (kg)  │   Threats     │       Total         │
│     15%       │      25       │      12       │       0       │         5           │
├───────────────┼───────────────┼───────────────┼───────────────┼─────────────────────┤
│ Baseline kWh  │      Min      │   Per kWh     │    Blocked    │       Online        │
│    2500       │      20       │     0.4       │       0       │         5           │
├───────────────┼───────────────┼───────────────┼───────────────┼─────────────────────┤
│ Current kWh   │      Max      │ Trees Equiv.  │   Accuracy    │      Avg CPU        │
│    2125       │      30       │     0.5       │    98.5%      │        45%          │
└───────────────┴───────────────┴───────────────┴───────────────┴─────────────────────┘

Before:
<img width="2048" height="1210" alt="Before" src="https://github.com/user-attachments/assets/a27284c5-17c3-4021-bec5-19235342d2c7" />



After:
<img width="2056" height="1329" alt="After" src="https://github.com/user-attachments/assets/2206f7be-c3eb-41c6-ac1a-4d413dd2c020" />






```

### Calculation Formulas

#### 1. Energy Reduction Percentage

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        ENERGY REDUCTION FORMULA                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                     Baseline kWh - Current kWh                                       │
│   Reduction % = ────────────────────────────────── × 100                            │
│                          Baseline kWh                                                │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   EXAMPLE:                                                                           │
│                                                                                      │
│                     2500 - 2125                                                      │
│   Reduction % = ───────────────── × 100 = 15%                                       │
│                        2500                                                          │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 2. Current Energy Consumption

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        CURRENT CONSUMPTION FORMULA                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   Current kWh = Baseline kWh × (1 - Reduction% / 100)                               │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   EXAMPLE:                                                                           │
│                                                                                      │
│   Current kWh = 2500 × (1 - 15/100) = 2500 × 0.85 = 2125 kWh                        │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3. Monthly Cost Savings

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        COST SAVINGS FORMULA                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   Monthly Savings (AZN) = (Baseline kWh - Current kWh) × Cost per kWh               │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   EXAMPLE:                                                                           │
│                                                                                      │
│   Monthly Savings = (2500 - 2125) × 0.10 AZN                                        │
│   Monthly Savings = 375 × 0.10 = 37.50 AZN                                          │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   PARAMETERS:                                                                        │
│   • Cost per kWh = 0.10 AZN (configurable in metrics.json)                          │
│   • Baseline kWh = 2500 (monthly baseline consumption)                              │
│   • Current kWh = Actual consumption after optimization                             │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4. CO2 Reduction

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        CO2 REDUCTION FORMULA                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   CO2 Reduction (kg) = (Baseline kWh - Current kWh) × CO2 per kWh                   │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   EXAMPLE:                                                                           │
│                                                                                      │
│   CO2 Reduction = (2500 - 2125) × 0.4 kg/kWh                                        │
│   CO2 Reduction = 375 × 0.4 = 150 kg                                                │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   PARAMETERS:                                                                        │
│   • CO2 per kWh = 0.4 kg (average carbon emission factor)                           │
│   • Based on regional electricity grid carbon intensity                             │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 5. Trees Equivalent

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        TREES EQUIVALENT FORMULA                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   Trees Equivalent = CO2 Reduction (kg) / 21                                        │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   EXAMPLE:                                                                           │
│                                                                                      │
│   Trees = 150 kg / 21 = 7.14 trees                                                  │
│                                                                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│   NOTE: One tree absorbs approximately 21 kg of CO2 per year                        │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6. Complete Calculation Summary

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE ENERGY EFFICIENCY CALCULATION                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   INPUT PARAMETERS:                                                                  │
│   ├── Baseline Consumption:    2500 kWh/month                                       │
│   ├── Current Consumption:     2125 kWh/month                                       │
│   ├── Cost per kWh:            0.10 AZN                                             │
│   └── CO2 per kWh:             0.40 kg                                              │
│                                                                                      │
│   CALCULATED RESULTS:                                                                │
│   ├── Energy Saved:            375 kWh (2500 - 2125)                                │
│   ├── Reduction Percentage:    15% ((375/2500) × 100)                               │
│   ├── Monthly Cost Savings:    37.50 AZN (375 × 0.10)                               │
│   ├── CO2 Reduction:           150 kg (375 × 0.40)                                  │
│   └── Trees Equivalent:        7.14 trees (150 / 21)                                │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure

```
final_configuration/
│
├── 📄 prometheus.yml              # Prometheus configuration
│   └── Location: /etc/prometheus/prometheus.yml
│
├── 📄 alerts.yml                  # Alert rules
│   └── Location: /etc/prometheus/rules/alerts.yml
│
├── 📄 metrics.json                # KPI values (EDIT THIS!)
│   └── Location: /opt/monitoring/metrics.json
│
├── 🐍 metrics_exporter.py         # Python: JSON → Prometheus
│   └── Location: /opt/monitoring/metrics_exporter.py
│
├── 🐍 service_checker.py          # Python: Service monitoring
│   └── Location: /opt/monitoring/service_checker.py
│
├── 📄 grafana-dashboard.json      # Pre-built Grafana dashboard
│   └── Import via Grafana UI
│
├── 📄 mock_metrics_server.js      # Node.js: Test data generator
│   └── Location: /opt/monitoring/mock_metrics_server.js
│
├── 📄 package.json                # Node.js dependencies
│
├── 📄 README.md                   # This documentation
│
└── 📄 Infrastructure_Monitoring_Presentation.pptx
    └── Presentation slides for management
```

### File Details

| File | Size | Purpose | Editable |
|------|------|---------|----------|
| prometheus.yml | 7 KB | Scrape configuration | ✓ |
| alerts.yml | 5 KB | Alert rules | ✓ |
| metrics.json | 1 KB | KPI values | ✓ (Primary) |
| metrics_exporter.py | 6 KB | JSON to Prometheus | ✗ |
| service_checker.py | 11 KB | Service monitoring | ✓ (Services list) |
| grafana-dashboard.json | 18 KB | Dashboard definition | ✗ |
| mock_metrics_server.js | 2 KB | Test data | ✓ |

---

## 🚀 Installation Guide

### Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| RHEL/CentOS | 9.x | `cat /etc/redhat-release` |
| Python | 3.9+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| Prometheus | 2.x | `prometheus --version` |
| Grafana | 10.x | `grafana-server -v` |

### Step 1: Install Prometheus

```bash
# Add Prometheus user
sudo useradd --no-create-home --shell /bin/false prometheus

# Create directories
sudo mkdir -p /etc/prometheus /var/lib/prometheus

# Download and install
cd /tmp
wget https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz
tar xvf prometheus-2.47.0.linux-amd64.tar.gz
cd prometheus-2.47.0.linux-amd64

# Copy binaries
sudo cp prometheus promtool /usr/local/bin/
sudo cp -r consoles console_libraries /etc/prometheus/

# Set ownership
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
```

### Step 2: Install Grafana

```bash
# Add Grafana repository
sudo tee /etc/yum.repos.d/grafana.repo << 'EOF'
[grafana]
name=grafana
baseurl=https://rpm.grafana.com
repo_gpgcheck=1
enabled=1
gpgcheck=1
gpgkey=https://rpm.grafana.com/gpg.key
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
EOF

# Install
sudo dnf install grafana -y

# Enable and start
sudo systemctl enable --now grafana-server
```

### Step 3: Install Node Exporter

```bash
# Download and install
cd /tmp
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvf node_exporter-1.6.1.linux-amd64.tar.gz

# Copy binary
sudo cp node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/

# Create systemd service
sudo tee /etc/systemd/system/node_exporter.service << 'EOF'
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable --now node_exporter
```

### Step 4: Copy Configuration Files

```bash
# Create directories
sudo mkdir -p /etc/prometheus/rules
sudo mkdir -p /opt/monitoring

# Copy Prometheus configuration
sudo cp prometheus.yml /etc/prometheus/prometheus.yml
sudo cp alerts.yml /etc/prometheus/rules/alerts.yml

# Copy monitoring scripts
sudo cp metrics.json /opt/monitoring/
sudo cp metrics_exporter.py /opt/monitoring/
sudo cp service_checker.py /opt/monitoring/
sudo cp mock_metrics_server.js /opt/monitoring/
sudo cp package.json /opt/monitoring/

# Set permissions
sudo chown -R prometheus:prometheus /etc/prometheus
sudo chmod 755 /opt/monitoring/*.py
```

### Step 5: Install Python Dependencies

```bash
# Install prometheus_client
sudo pip3 install prometheus_client requests

# Or using virtual environment
cd /opt/monitoring
python3 -m venv venv
source venv/bin/activate
pip install prometheus_client requests
```

### Step 6: Install Node.js Dependencies

```bash
cd /opt/monitoring
npm install
```

### Step 7: Create Systemd Services

#### Prometheus Service
```bash
sudo tee /etc/systemd/system/prometheus.service << 'EOF'
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries \
    --web.enable-lifecycle
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

#### Metrics Exporter Service
```bash
sudo tee /etc/systemd/system/metrics-exporter.service << 'EOF'
[Unit]
Description=Metrics Exporter for Prometheus
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/monitoring
ExecStart=/usr/bin/python3 /opt/monitoring/metrics_exporter.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

#### Service Checker Service
```bash
sudo tee /etc/systemd/system/service-checker.service << 'EOF'
[Unit]
Description=Service Checker for Prometheus
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/monitoring
ExecStart=/usr/bin/python3 /opt/monitoring/service_checker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

#### Mock Metrics Server Service (Optional)
```bash
sudo tee /etc/systemd/system/mock-metrics.service << 'EOF'
[Unit]
Description=Mock Metrics Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/monitoring
ExecStart=/usr/bin/node /opt/monitoring/mock_metrics_server.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

### Step 8: Start All Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start services
sudo systemctl enable --now prometheus
sudo systemctl enable --now grafana-server
sudo systemctl enable --now node_exporter
sudo systemctl enable --now metrics-exporter
sudo systemctl enable --now service-checker
sudo systemctl enable --now mock-metrics  # Optional

# Verify all services
sudo systemctl status prometheus grafana-server node_exporter metrics-exporter service-checker
```

### Step 9: Configure Firewall

```bash
# Open required ports
sudo firewall-cmd --permanent --add-port=9090/tcp  # Prometheus
sudo firewall-cmd --permanent --add-port=3000/tcp  # Grafana
sudo firewall-cmd --permanent --add-port=9100/tcp  # Node Exporter
sudo firewall-cmd --permanent --add-port=9101/tcp  # Metrics Exporter
sudo firewall-cmd --permanent --add-port=9102/tcp  # Service Checker
sudo firewall-cmd --permanent --add-port=9200/tcp  # Mock Server

# Reload firewall
sudo firewall-cmd --reload
```

---

## 📊 Grafana Setup

### Step 1: Login to Grafana

```
URL: http://172.31.3.177:3000
Username: admin
Password: admin (change on first login)
```

### Step 2: Add Prometheus Data Source

1. Navigate to **Configuration** → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Configure:
   ```
   Name: Prometheus
   URL: http://localhost:9090
   ```
5. Click **Save & Test**
6. Verify: "Data source is working"

### Step 3: Import Dashboard

1. Navigate to **Dashboards** → **Import**
2. Click **Upload JSON file**
3. Select `grafana-dashboard.json`
4. Select **Prometheus** as data source
5. Click **Import**

### Dashboard Structure

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE MONITORING DASHBOARD                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ROW 1: KEY ACHIEVEMENTS                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                             │
│  │  Energy  │  │   Cost   │  │   CO2    │  │ Security │                             │
│  │ Reduction│  │ Savings  │  │Reduction │  │ Threats  │                             │
│  │  Gauge   │  │  Stat    │  │  Gauge   │  │  Stat    │                             │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ROW 2: SERVER METRICS                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                             │
│  │ Avg CPU  │  │Avg Memory│  │ Avg Temp │  │ Servers  │                             │
│  │  Gauge   │  │  Gauge   │  │  Gauge   │  │  Online  │                             │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ROW 3: SERVICE STATUS                                                               │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐                   │
│  │      Service Status         │  │   Services Over Time        │                   │
│  │   (Stat with UP/DOWN)       │  │   (Time Series Graph)       │                   │
│  └─────────────────────────────┘  └─────────────────────────────┘                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ROW 4: SYSTEM METRICS                                                               │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐                   │
│  │    CPU Usage Over Time      │  │  Memory Usage Over Time     │                   │
│  │     (Time Series)           │  │     (Time Series)           │                   │
│  └─────────────────────────────┘  └─────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration

### Editing metrics.json

The `metrics.json` file controls all KPI values displayed in Grafana.

**Location:** `/opt/monitoring/metrics.json`

```json
{
  "energy": {
    "reduction_percent": 15,        // ← Edit this value
    "baseline_kwh": 2500,
    "current_kwh": 2125,
    "target_reduction_percent": 20
  },
  "cost_savings": {
    "monthly_savings": 25,          // ← Or this value
    "min_savings": 20,
    "max_savings": 30,
    "cost_per_kwh": 0.10
  },
  "co2_reduction": {
    "monthly_reduction_kg": 12,
    "co2_per_kwh": 0.4,
    "trees_equivalent": 0.5
  },
  "security": {
    "threats_detected": 0,
    "threats_blocked": 0,
    "requests_scanned": 15000,
    "accuracy_percent": 98.5
  },
  "servers": {
    "total_monitored": 5,
    "online": 5,
    "avg_cpu_percent": 45,
    "avg_memory_percent": 62
  }
}
```

**After editing:** Changes appear in Grafana within 30 seconds automatically.

### Editing Service List

**File:** `/opt/monitoring/service_checker.py`

```python
SERVICES_TO_MONITOR = [
    'prometheus',
    'grafana-server',
    'node_exporter',
    'nginx',
    'postgresql',
    'sshd',
    # Add your services here
]
```

**After editing:** Restart the service checker:
```bash
sudo systemctl restart service-checker
```

---

## 🚨 Alert Rules

### Configured Alerts

| Alert Name | Condition | Severity | Description |
|------------|-----------|----------|-------------|
| TargetDown | `up == 0` | Critical | Monitoring target unreachable |
| HighCPU | `CPU > 80%` for 5m | Warning | High CPU utilization |
| HighMemory | `Memory > 85%` for 5m | Warning | High memory utilization |
| LowDisk | `Disk < 20%` | Warning | Low disk space |
| ServiceDown | `service_status == 0` | Critical | Service stopped |
| SecurityThreat | `threats > 0` | Critical | Security threat detected |

### Alert Rule Definitions

```yaml
# File: /etc/prometheus/rules/alerts.yml

groups:
  - name: target_alerts
    rules:
      - alert: TargetDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Target {{ $labels.job }} is DOWN"

  - name: system_alerts
    rules:
      - alert: HighCPU
        expr: 100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning

      - alert: HighMemory
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
```

---

## 🔌 API Endpoints

### Prometheus Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/query` | GET | Execute PromQL query |
| `/api/v1/query_range` | GET | Query over time range |
| `/api/v1/targets` | GET | List all targets |
| `/api/v1/alerts` | GET | List all alerts |
| `/api/v1/rules` | GET | List all rules |
| `/-/reload` | POST | Reload configuration |

**Example Queries:**
```bash
# Get energy reduction
curl 'http://localhost:9090/api/v1/query?query=achievement_energy_reduction_percent'

# Get all targets
curl 'http://localhost:9090/api/v1/targets'

# Reload configuration
curl -X POST http://localhost:9090/-/reload
```

### Exporter Endpoints

| Service | Endpoint | Description |
|---------|----------|-------------|
| Metrics Exporter | `http://localhost:9101/metrics` | KPI metrics |
| Service Checker | `http://localhost:9102/metrics` | Service status |
| Node Exporter | `http://localhost:9100/metrics` | System metrics |
| Mock Server | `http://localhost:9200/metrics-json` | JSON test data |

---

## 📸 Screenshots

### Dashboard Overview

The Grafana dashboard displays all KPIs in an easy-to-read format:

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        GRAFANA DASHBOARD - KPI OVERVIEW                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐            │
│   │   ENERGY    │   │    COST     │   │     CO2     │   │  SECURITY   │            │
│   │             │   │   SAVINGS   │   │  REDUCTION  │   │             │            │
│   │    ████     │   │             │   │    ████     │   │             │            │
│   │   █████     │   │     25      │   │   █████     │   │      0      │            │
│   │    15%      │   │     AZN     │   │    12 kg    │   │   THREATS   │            │
│   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘            │
│                                                                                      │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐            │
│   │  AVG CPU    │   │ AVG MEMORY  │   │  AVG TEMP   │   │  SERVERS    │            │
│   │             │   │             │   │             │   │   ONLINE    │            │
│   │    ████     │   │   █████     │   │   ████      │   │             │            │
│   │    45%      │   │    62%      │   │    52°C     │   │     5/5     │            │
│   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘            │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Prometheus Targets

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           PROMETHEUS TARGETS STATUS                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   Endpoint                          State     Labels                   Last Scrape  │
│   ─────────────────────────────────────────────────────────────────────────────────  │
│   http://localhost:9090/metrics     UP        job="prometheus"         2s ago       │
│   http://localhost:9100/metrics     UP        job="node-exporter"      5s ago       │
│   http://localhost:9101/metrics     UP        job="metrics-exporter"   3s ago       │
│   http://localhost:9102/metrics     UP        job="service-checker"    8s ago       │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Service Status Panel

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SERVICE STATUS                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                  │
│   │   prometheus     │  │  grafana-server  │  │  node_exporter   │                  │
│   │       UP ✓       │  │       UP ✓       │  │       UP ✓       │                  │
│   │    (green)       │  │    (green)       │  │    (green)       │                  │
│   └──────────────────┘  └──────────────────┘  └──────────────────┘                  │
│                                                                                      │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                  │
│   │      nginx       │  │    postgresql    │  │       sshd       │                  │
│   │       UP ✓       │  │       UP ✓       │  │       UP ✓       │                  │
│   │    (green)       │  │    (green)       │  │    (green)       │                  │
│   └──────────────────┘  └──────────────────┘  └──────────────────┘                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Quick Reference

### Port Summary

| Port | Service | URL |
|------|---------|-----|
| 9090 | Prometheus | http://172.31.3.177:9090 |
| 3000 | Grafana | http://172.31.3.177:3000 |
| 9100 | Node Exporter | http://172.31.3.177:9100/metrics |
| 9101 | Metrics Exporter | http://172.31.3.177:9101/metrics |
| 9102 | Service Checker | http://172.31.3.177:9102/metrics |
| 9200 | Mock Server | http://172.31.3.177:9200/metrics-json |

### Quick Commands

```bash
# Restart all services
sudo systemctl restart prometheus grafana-server node_exporter metrics-exporter service-checker

# Check all services
sudo systemctl status prometheus grafana-server node_exporter metrics-exporter service-checker

# View logs
sudo journalctl -u prometheus -f
sudo journalctl -u metrics-exporter -f

# Test metrics
curl http://localhost:9101/metrics | grep achievement
curl http://localhost:9102/metrics | grep service

# Reload Prometheus config
curl -X POST http://localhost:9090/-/reload

# Edit KPIs
sudo nano /opt/monitoring/metrics.json
```

---

## 📄 License

This project is provided as-is for internal use.

**Author:** Aykhan
**Version:** 3.1
**Last Updated:** February 2026

---

<p align="center">
  <strong>Infrastructure Monitoring System</strong><br>
  <em>Built with Prometheus • Grafana • Python • Node.js</em>
</p>
