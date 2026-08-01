import json
import urllib.request
from typing import Dict, Any


class QANotifier:
    """Sends real-time QA alert notifications to Webhooks (Slack / Discord / Teams)."""

    @staticmethod
    def send_webhook_alert(webhook_url: str, test_summary: Dict[str, Any]) -> bool:
        """Publishes formatted test execution alerts to webhooks."""
        pass_rate = test_summary.get("pass_rate", 0.0)
        status_color = "#36a64f" if pass_rate >= 80.0 else "#FF0000"
        status_text = "PASSED" if pass_rate >= 80.0 else "FAILED / RISK DETECTED"

        payload = {
            "text": f"🚨 *AITestKit QA Execution Alert — Status: {status_text}*",
            "attachments": [
                {
                    "color": status_color,
                    "fields": [
                        {"title": "Domain Context", "value": test_summary.get("domain", "N/A"), "short": True},
                        {"title": "Pass Rate", "value": f"{pass_rate:.1f}%", "short": True},
                        {"title": "Total Executed", "value": str(test_summary.get("total", 0)), "short": True},
                        {"title": "Passed Tests", "value": str(test_summary.get("passed", 0)), "short": True},
                        {"title": "Failed Tests", "value": str(test_summary.get("failed", 0)), "short": True}
                    ],
                    "footer": "AITestKit Automated QA Engine v0.1.0"
                }
            ]
        }

        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except Exception:
            return False