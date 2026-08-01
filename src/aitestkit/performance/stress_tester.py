import time
from typing import Callable, Dict, Any
from aitestkit.performance.load_tester import LoadTester

class StressTester:
    """Ramps up load iteratively until system reaches breaking point/failure threshold."""

    def find_breaking_point(
        self, 
        target_func: Callable[[], Any], 
        start_users: int = 5, 
        max_users: int = 100, 
        step: int = 10
    ) -> Dict[str, Any]:
        
        load_engine = LoadTester()
        current_users = start_users
        breaking_user_count = None
        run_history = []

        while current_users <= max_users:
            res = load_engine.execute_load_test(target_func, concurrent_users=current_users, total_requests=current_users * 2)
            run_history.append(res)
            
            # Failure criteria: success rate < 95% or avg latency > 2.0s
            if res["success_rate"] < 95.0 or res["avg_latency_sec"] > 2.0:
                breaking_user_count = current_users
                break
            
            current_users += step

        return {
            "max_tested_users": current_users if not breaking_user_count else breaking_user_count,
            "breaking_point_detected": breaking_user_count is not None,
            "breaking_user_capacity": breaking_user_count or max_users,
            "stress_stages": run_history
        }