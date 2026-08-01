import time
import psutil
from typing import Callable, Dict, Any, List


class LongevityLeakScanner:
    """Monitors CPU, System RAM, and Memory drift during prolonged execution runs."""

    @staticmethod
    def run_longevity_scan(target_func: Callable[[], Any], iterations: int = 50, delay_sec: float = 0.01) -> Dict[str, Any]:
        process = psutil.Process()
        
        initial_ram_mb = process.memory_info().rss / (1024 * 1024)
        ram_samples: List[float] = []
        cpu_samples: List[float] = []

        for _ in range(iterations):
            target_func()
            time.sleep(delay_sec)
            ram_samples.append(process.memory_info().rss / (1024 * 1024))
            cpu_samples.append(process.cpu_percent(interval=None))

        final_ram_mb = ram_samples[-1] if ram_samples else initial_ram_mb
        peak_ram_mb = max(ram_samples) if ram_samples else initial_ram_mb
        ram_drift_mb = final_ram_mb - initial_ram_mb

        # Memory leak detected if RAM drift > 5MB over test run
        has_memory_leak = ram_drift_mb > 5.0

        return {
            "iterations_executed": iterations,
            "initial_ram_mb": round(initial_ram_mb, 2),
            "final_ram_mb": round(final_ram_mb, 2),
            "peak_ram_mb": round(peak_ram_mb, 2),
            "ram_drift_mb": round(ram_drift_mb, 2),
            "avg_cpu_percent": round(sum(cpu_samples) / len(cpu_samples), 2) if cpu_samples else 0.0,
            "memory_leak_detected": has_memory_leak,
            "status": "FAILED (Memory Leak)" if has_memory_leak else "PASSED (Stable)"
        }