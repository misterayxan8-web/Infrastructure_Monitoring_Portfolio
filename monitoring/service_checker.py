#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SERVICE CHECKER FOR PROMETHEUS                            ║
║                    Monitors systemd services → Exposes metrics               ║
║                    Author: Aykhan | Version: 3.0                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

WHAT THIS SCRIPT DOES:
----------------------
1. Checks if important services are running (systemd)
2. Measures how long each service has been running
3. Exposes this data to Prometheus on port 9102
4. You can create alerts when services go down!

Hds = how long the check took
"""

import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================================================
# CONFIGURATION - Edit this list with your services!
# ============================================================================

SERVICES_TO_MONITOR = [
    # Add services you want to monitor
    # These are checked using: systemctl is-active SERVICE_NAME

    # --- MONITORING SERVICES ---
    'prometheus',
    'grafana-server',
    'node_exporter',

    # --- WEB SERVICES ---
    'nginx',
    'httpd',          # Apache

    # --- DATABASE SERVICES ---
    'postgresql',
    'mariadb',
    'redis',

    # --- SYSTEM SERVICES ---
    'sshd',
    'firewalld',
    'crond',

    # --- UNCOMMENT SERVICES YOU USE ---
    # 'docker',
    # 'containerd',
    # 'mysql',
    # 'mongodb',
    # 'elasticsearch',
    # 'rabbitmq-server',
]

# Port for this exporter
EXPORTER_PORT = 9102

# How often to check services (seconds)
CHECK_INTERVAL = 30

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================================
# SERVICE CHECKER CLASS
# ============================================================================

class ServiceChecker:
    """Checks status of systemd services."""

    def __init__(self, services):
        self.services = services
        self.last_check_time = 0
        self.last_check_duration = 0
        self.service_statuses = {}
        self.service_uptimes = {}

    def check_service(self, service_name):
        """Check if a service is running using systemctl."""
        try:
            # Check if service is active
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            is_running = result.returncode == 0

            # Get uptime if running
            uptime = 0
            if is_running:
                try:
                    result = subprocess.run(
                        ['systemctl', 'show', service_name, '--property=ActiveEnterTimestamp'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    # Parse timestamp: ActiveEnterTimestamp=Thu 2024-01-01 10:00:00 UTC
                    timestamp_str = result.stdout.strip().split('=', 1)[-1]
                    if timestamp_str and timestamp_str != 'n/a':
                        # Try to calculate uptime
                        try:
                            from datetime import datetime
                            # Simple uptime estimation
                            uptime = time.time() - self.last_check_time if self.last_check_time > 0 else 0
                        except:
                            pass
                except:
                    pass

            return is_running, uptime

        except subprocess.TimeoutExpired:
            logger.warning(f"Timeout checking {service_name}")
            return False, 0
        except FileNotFoundError:
            logger.error("systemctl not found - are you on a systemd system?")
            return False, 0
        except Exception as e:
            logger.error(f"Error checking {service_name}: {e}")
            return False, 0

    def check_all_services(self):
        """Check all configured services."""
        start_time = time.time()

        for service in self.services:
            is_running, uptime = self.check_service(service)
            self.service_statuses[service] = 1 if is_running else 0
            self.service_uptimes[service] = uptime

        self.last_check_duration = time.time() - start_time
        self.last_check_time = time.time()

        # Log summary
        running = sum(1 for s in self.service_statuses.values() if s == 1)
        total = len(self.services)
        logger.info(f"Service check complete: {running}/{total} running")

    def format_metrics(self):
        """Format metrics in Prometheus format."""
        lines = []

        # Header
        lines.append("# Service Checker Metrics")
        lines.append(f"# Generated: {datetime.now().isoformat()}")
        lines.append("")

        # Exporter info
        lines.append("# HELP service_checker_info Information about this exporter")
        lines.append("# TYPE service_checker_info gauge")
        lines.append('service_checker_info{version="3.0",author="Aykhan"} 1')
        lines.append("")

        # Service status (1=running, 0=stopped)
        lines.append("# HELP service_status Service status (1=running, 0=stopped)")
        lines.append("# TYPE service_status gauge")
        for service, status in self.service_statuses.items():
            lines.append(f'service_status{{service="{service}"}} {status}')
        lines.append("")

        # Service uptime
        lines.append("# HELP service_uptime_seconds Service uptime in seconds")
        lines.append("# TYPE service_uptime_seconds gauge")
        for service, uptime in self.service_uptimes.items():
            lines.append(f'service_uptime_seconds{{service="{service}"}} {uptime}')
        lines.append("")

        # Check duration
        lines.append("# HELP service_check_duration_seconds Duration of last check")
        lines.append("# TYPE service_check_duration_seconds gauge")
        lines.append(f'service_check_duration_seconds {self.last_check_duration:.4f}')
        lines.append("")

        # Total services
        lines.append("# HELP services_total Total number of monitored services")
        lines.append("# TYPE services_total gauge")
        lines.append(f'services_total {len(self.services)}')
        lines.append("")

        # Services running
        running = sum(1 for s in self.service_statuses.values() if s == 1)
        lines.append("# HELP services_running Number of running services")
        lines.append("# TYPE services_running gauge")
        lines.append(f'services_running {running}')
        lines.append("")

        # Last check timestamp
        lines.append("# HELP service_check_timestamp_seconds Timestamp of last check")
        lines.append("# TYPE service_check_timestamp_seconds gauge")
        lines.append(f'service_check_timestamp_seconds {self.last_check_time}')
        lines.append("")

        return '\n'.join(lines)

# ============================================================================
# HTTP HANDLER
# ============================================================================

# Global checker instance
checker = None

class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP handler for /metrics endpoint."""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/metrics':
            metrics = checker.format_metrics()
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(metrics.encode('utf-8'))

        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"healthy"}')

        elif self.path == '/':
            html = """
            <html>
            <head><title>Service Checker</title></head>
            <body>
                <h1>Service Checker Exporter</h1>
                <p><a href="/metrics">/metrics</a> - Prometheus metrics</p>
                <p><a href="/health">/health</a> - Health check</p>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function."""
    global checker

    print("=" * 60)
    print("  SERVICE CHECKER FOR PROMETHEUS")
    print("  Author: Aykhan | Version: 3.0")
    print("=" * 60)
    print(f"  Port: {EXPORTER_PORT}")
    print(f"  Services monitored: {len(SERVICES_TO_MONITOR)}")
    print(f"  Check interval: {CHECK_INTERVAL}s")
    print("=" * 60)
    print("\n  Monitored services:")
    for svc in SERVICES_TO_MONITOR:
        print(f"    - {svc}")
    print()

    # Initialize checker
    checker = ServiceChecker(SERVICES_TO_MONITOR)

    # Initial check
    checker.check_all_services()

    # Start HTTP server in background
    server_address = ('', EXPORTER_PORT)
    httpd = HTTPServer(server_address, MetricsHandler)

    logger.info(f"Exporter started on http://localhost:{EXPORTER_PORT}/metrics")
    print("  READY! Check http://localhost:{}/metrics".format(EXPORTER_PORT))
    print("  Press Ctrl+C to stop")
    print()

    # Run server with periodic checks
    import threading

    def check_loop():
        while True:
            time.sleep(CHECK_INTERVAL)
            checker.check_all_services()

    check_thread = threading.Thread(target=check_loop, daemon=True)
    check_thread.start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        print("\nService checker stopped.")

if __name__ == '__main__':
    main()

