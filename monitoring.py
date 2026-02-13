class MonitoringService:
    def __init__(self):
        self.bandwidth_limit = 100  # Example limit in Mbps
        self.concurrent_devices = []
        self.suspicious_activity_logs = []

    def check_bandwidth_limit(self, currently_used_bandwidth):
        """Check if the current bandwidth usage exceeds the limit."""
        if currently_used_bandwidth > self.bandwidth_limit:
            return True
        return False

    def monitor_concurrent_devices(self, device):
        """Add device to the concurrent device list if not already present."""
        if device not in self.concurrent_devices:
            self.concurrent_devices.append(device)

    def detect_suspicious_activity(self, activity):
        """Log activity as suspicious if it meets certain criteria."""
        if activity['type'] == 'unauthorized_access':
            self.suspicious_activity_logs.append(activity)

    def send_email_alert(self, alert_message):
        """Send an email alert with the provided message."""
        print(f"Sending email alert: {alert_message}")  # Placeholder for email sending logic

    def generate_alert_report(self):
        """Generate a report of all suspicious activities logged."""
        report = "Suspicious Activity Report:\n"
        for log in self.suspicious_activity_logs:
            report += f"{log}\n"
        return report
