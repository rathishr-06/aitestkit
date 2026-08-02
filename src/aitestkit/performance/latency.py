import time
from typing import List, Dict, Any, Callable


class LatencyBenchmark:
    """Measures latency metrics including TTFT and percentiles."""

    @staticmethod
    def measure_function_latency(target_func: Callable[[], Any], samples: int = 10) -> Dict[str, Any]:
        """Executes function multiple times and calculates percentile latencies."""
        latencies: List[float] = []

        for _ in range(samples):
            start = time.perf_counter()
            target_func()
            end = time.perf_counter()
            latencies.append(end - start)

        latencies.sort()
        n = len(latencies)

        def get_percentile(p: float) -> float:
            idx = int(p * n)
            return latencies[min(idx, n - 1)]

        avg_latency = sum(latencies) / n if n > 0 else 0.0

        return {
            "samples": n,
            "avg_latency_sec": round(avg_latency, 4),
            "min_sec": round(latencies[0], 4) if n > 0 else 0.0,
            "max_sec": round(latencies[-1], 4) if n > 0 else 0.0,
            "p50_sec": round(get_percentile(0.50), 4),
            "p90_sec": round(get_percentile(0.90), 4),
            "p95_sec": round(get_percentile(0.95), 4),
            "p99_sec": round(get_percentile(0.99), 4),
        }