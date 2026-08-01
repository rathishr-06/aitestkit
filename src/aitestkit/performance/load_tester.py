import concurrent.futures
import time
from typing import Callable, Dict, Any, List

class LoadTester:
    """Multi-threaded concurrent user simulation engine."""

    def execute_load_test(
        self, 
        target_function: Callable[[], Any], 
        concurrent_users: int = 10, 
        total_requests: int = 50
    ) -> Dict[str, Any]:
        
        latencies: List[float] = []
        successes = 0
        failures = 0

        def worker():
            nonlocal successes, failures
            start = time.perf_counter()
            try:
                target_function()
                elapsed = time.perf_counter() - start
                latencies.append(elapsed)
                successes += 1
            except Exception:
                failures += 1

        start_total = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(worker) for _ in range(total_requests)]
            concurrent.futures.wait(futures)
        
        total_duration = time.perf_counter() - start_total
        latencies.sort()

        p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0.0
        p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0.0
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

        return {
            "concurrent_users": concurrent_users,
            "total_requests": total_requests,
            "success_rate": round((successes / total_requests) * 100, 2) if total_requests else 0,
            "throughput_rps": round(total_requests / total_duration, 2) if total_duration > 0 else 0,
            "avg_latency_sec": round(avg_latency, 4),
            "p95_sec": round(p95, 4),
            "p99_sec": round(p99, 4),
            "failures": failures
        }