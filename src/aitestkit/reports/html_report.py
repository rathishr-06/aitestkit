from pathlib import Path
from typing import Dict, Any

class HTMLReportGenerator:
    """Generates standalone interactive HTML reports for evaluation results."""

    @staticmethod
    def generate(data: Dict[str, Any], output_path: str = "reports/evaluation_report.html") -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AITestKit — Evaluation Report</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }}
                .card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid #334155; }}
                h1 {{ color: #38bdf8; }}
                h2 {{ color: #f43f5e; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; }}
                pre {{ background: #090d16; padding: 1rem; border-radius: 8px; color: #a7f3d0; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <h1>⚡ AITestKit Evaluation Report</h1>
            <p>Generated automatically by AITestKit Core Engine v0.1.0</p>
            <div class="card">
                <h2>Benchmark Metrics Summary</h2>
                <pre>{data}</pre>
            </div>
        </body>
        </html>
        """

        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)