from collections.abc import Callable, Generator
from typing import Any
from aitestkit.performance.system import (
    LatencyTracker,
    PerformanceMetrics,
    SystemMonitor,
)


class PerformanceEvaluator:
    """Evaluates synchronous, streaming, and API-based LLM outputs."""

    def __init__(self):
        self.monitor = SystemMonitor()

    def evaluate_stream(
        self, stream_func: Callable[[], Generator[str, None, None]]
    ) -> tuple[str, PerformanceMetrics]:
        """Evaluates a streaming function and measures TTFT, TPS, and Resource Usage."""
        tracker = LatencyTracker()
        monitor = SystemMonitor()

        cpu_start = monitor.get_cpu_usage()
        tracker.start()

        full_text = []
        token_count = 0

        for chunk in stream_func():
            tracker.record_first_token()
            full_text.append(chunk)
            token_count += 1  # Standard word/chunk token approximation

        tracker.stop()
        cpu_end = monitor.get_cpu_usage()

        total_latency, ttft, tps = tracker.calculate_metrics(token_count)
        avg_cpu = round((cpu_start + cpu_end) / 2, 2)

        metrics = PerformanceMetrics(
            total_latency=total_latency,
            ttft=ttft,
            tokens_per_second=tps,
            cpu_percent=avg_cpu,
            ram_usage_mb=monitor.get_ram_usage_mb(),
        )

        return "".join(full_text), metrics