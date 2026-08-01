from dataclasses import dataclass
import os
import psutil
import time


@dataclass
class PerformanceMetrics:
    total_latency: float  # Total execution time in seconds
    ttft: float  # Time to first token (seconds)
    tokens_per_second: float  # Generated tokens / total generation time
    cpu_percent: float  # Average CPU usage %
    ram_usage_mb: float  # RAM used in MB


class SystemMonitor:
    """Monitors system resources (CPU, RAM) during LLM execution."""

    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def get_cpu_usage(self) -> float:
        return psutil.cpu_percent(interval=None)

    def get_ram_usage_mb(self) -> float:
        return round(self.process.memory_info().rss / (1024 * 1024), 2)


class LatencyTracker:
    """Tracks latency metrics like TTFT, Total Time, and TPS."""

    def __init__(self):
        self._start_time = None
        self._first_token_time = None
        self._end_time = None

    def start(self):
        self._start_time = time.perf_counter()

    def record_first_token(self):
        if self._first_token_time is None:
            self._first_token_time = time.perf_counter()

    def stop(self):
        self._end_time = time.perf_counter()

    def calculate_metrics(self, token_count: int) -> tuple[float, float, float]:
        if not self._start_time or not self._end_time:
            raise ValueError("Tracker was not properly started or stopped.")

        total_latency = round(self._end_time - self._start_time, 4)

        if self._first_token_time:
            ttft = round(self._first_token_time - self._start_time, 4)
            gen_time = self._end_time - self._first_token_time
        else:
            ttft = total_latency
            gen_time = total_latency

        tps = (
            round(token_count / gen_time, 2)
            if gen_time > 0 and token_count > 0
            else 0.0
        )
        return total_latency, ttft, tps