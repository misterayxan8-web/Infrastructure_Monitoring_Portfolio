#!/usr/bin/env python3
"""
METRICS EXPORTER FOR PROMETHEUS
Reads JSON from HTTP endpoint → Exposes Prometheus metrics
Author: Aykhan | Fixed production version
"""

import logging
import sys
import time
import requests

from prometheus_client import start_http_server, Gauge, Info, Counter

# ============================================================================
# CONFIGURATION
# ============================================================================

EXPORTER_PORT = 9101
METRICS_URL = "http://172.31.3.177:9200/metrics-json"
RELOAD_INTERVAL = 10

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ============================================================================
# PROMETHEUS METRICS
# ============================================================================

energy_reduction = Gauge("achievement_energy_reduction_percent", "Energy reduction %")
energy_baseline = Gauge("achievement_energy_baseline_kwh", "Baseline kWh")
energy_current = Gauge("achievement_energy_current_kwh", "Current kWh")
energy_target = Gauge("achievement_energy_target_percent", "Target reduction %")

cost_savings = Gauge("achievement_cost_savings_azn", "Monthly savings AZN")
cost_min = Gauge("achievement_cost_min_azn", "Min savings AZN")
cost_max = Gauge("achievement_cost_max_azn", "Max savings AZN")

co2_reduction = Gauge("achievement_co2_reduction_kg", "CO2 reduction kg")
co2_trees = Gauge("achievement_co2_trees_equivalent", "Trees equivalent")

security_threats = Gauge("achievement_security_threats_detected", "Threats detected")
security_blocked = Gauge("achievement_security_threats_blocked", "Threats blocked")
security_scanned = Gauge("achievement_security_requests_scanned", "Requests scanned")
security_accuracy = Gauge("achievement_security_accuracy_percent", "Accuracy %")

servers_total = Gauge("achievement_servers_total", "Total servers")
servers_online = Gauge("achievement_servers_online", "Servers online")
servers_sleep = Gauge("achievement_servers_sleep_mode", "Servers sleep")
avg_cpu = Gauge("achievement_avg_cpu_percent", "Avg CPU %")
avg_memory = Gauge("achievement_avg_memory_percent", "Avg memory %")
avg_temperature = Gauge("achievement_avg_temperature_celsius", "Avg temp °C")

threshold_cpu_warn = Gauge("threshold_cpu_warning_percent", "CPU warn %")
threshold_cpu_crit = Gauge("threshold_cpu_critical_percent", "CPU critical %")
threshold_memory_warn = Gauge("threshold_memory_warning_percent", "Memory warn %")
threshold_temp_warn = Gauge("threshold_temperature_warning_celsius", "Temp warn °C")

exporter_info = Info("metrics_exporter", "Exporter information")
config_reloads = Counter("metrics_exporter_reloads_total", "Reload count")

# ============================================================================
# LOAD METRICS FROM HTTP
# ============================================================================

def load_metrics():
    try:
        response = requests.get(METRICS_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        energy = data.get("energy", {})
        energy_reduction.set(energy.get("reduction_percent", 0))
        energy_baseline.set(energy.get("baseline_kwh", 0))
        energy_current.set(energy.get("current_kwh", 0))
        energy_target.set(energy.get("target_reduction_percent", 0))

        cost = data.get("cost_savings", {})
        cost_savings.set(cost.get("monthly_savings", 0))
        cost_min.set(cost.get("min_savings", 0))
        cost_max.set(cost.get("max_savings", 0))

        co2 = data.get("co2_reduction", {})
        co2_reduction.set(co2.get("monthly_reduction_kg", 0))
        co2_trees.set(co2.get("trees_equivalent", 0))

        security = data.get("security", {})
        security_threats.set(security.get("threats_detected", 0))
        security_blocked.set(security.get("threats_blocked", 0))
        security_scanned.set(security.get("requests_scanned", 0))
        security_accuracy.set(security.get("accuracy_percent", 0))

        servers = data.get("servers", {})
        servers_total.set(servers.get("total_monitored", 0))
        servers_online.set(servers.get("online", 0))
        servers_sleep.set(servers.get("in_sleep_mode", 0))
        avg_cpu.set(servers.get("avg_cpu_percent", 0))
        avg_memory.set(servers.get("avg_memory_percent", 0))
        avg_temperature.set(servers.get("avg_temperature_celsius", 0))

        thresholds = data.get("thresholds", {})
        threshold_cpu_warn.set(thresholds.get("cpu_warning", 80))
        threshold_cpu_crit.set(thresholds.get("cpu_critical", 95))
        threshold_memory_warn.set(thresholds.get("memory_warning", 85))
        threshold_temp_warn.set(thresholds.get("temperature_warning", 70))

        config_reloads.inc()
        logger.info("Metrics loaded successfully from HTTP endpoint")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("  METRICS EXPORTER FOR PROMETHEUS")
    print("  Fixed production version")
    print("=" * 60)
    print(f"  Port: {EXPORTER_PORT}")
    print(f"  Metrics URL: {METRICS_URL}")
    print(f"  Reload interval: {RELOAD_INTERVAL}s")
    print("=" * 60)

    exporter_info.info(
        {"version": "fixed", "metrics_url": METRICS_URL, "port": str(EXPORTER_PORT)}
    )

    if not load_metrics():
        logger.warning("Initial load failed — will retry")

    start_http_server(EXPORTER_PORT)
    logger.info(f"Exporter running on http://localhost:{EXPORTER_PORT}/metrics")

    while True:
        time.sleep(RELOAD_INTERVAL)
        load_metrics()


if __name__ == "__main__":
    main()

