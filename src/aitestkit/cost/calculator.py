from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class CostEstimate:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_per_request: float
    cost_per_1k_requests: float
    estimated_monthly_cost: float
    model_name: str
    optimization_tips: List[str]

class CostIntelligenceEngine:
    """Calculates LLM API token consumption, pricing, and monthly forecasts."""

    # Standard Model Pricing per 1k tokens (Prompt, Completion) in USD
    PRICING_TABLE = {
        "gpt-4o": {"prompt": 0.0025, "completion": 0.0100},
        "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
        "claude-3-5-sonnet": {"prompt": 0.0030, "completion": 0.0150},
        "llama-3-8b": {"prompt": 0.0000, "completion": 0.0000},  # Local/Self-hosted
        "deepseek-r1": {"prompt": 0.00055, "completion": 0.00219},
        "qwen-2.5-7b": {"prompt": 0.0000, "completion": 0.0000}
    }

    @classmethod
    def calculate_cost(
        cls, 
        prompt_tokens: int, 
        completion_tokens: int, 
        model_name: str = "gpt-4o-mini",
        monthly_requests_estimate: int = 100000
    ) -> CostEstimate:
        model_key = model_name.lower().strip()
        rates = cls.PRICING_TABLE.get(model_key, {"prompt": 0.0005, "completion": 0.0015})

        prompt_cost = (prompt_tokens / 1000.0) * rates["prompt"]
        completion_cost = (completion_tokens / 1000.0) * rates["completion"]
        cost_per_request = prompt_cost + completion_cost
        
        cost_per_1k = cost_per_request * 1000.0
        monthly_cost = cost_per_request * monthly_requests_estimate

        tips = []
        if prompt_tokens > 2000:
            tips.append("High prompt token count detected. Consider semantic context trimming or RAG top-k reduction.")
        if model_key in ["gpt-4o", "claude-3-5-sonnet"]:
            tips.append("Consider routing classification or simple queries to lightweight models like gpt-4o-mini or local quantized Llama-3.")
        if not tips:
            tips.append("Token usage and pricing are within optimal thresholds.")

        return CostEstimate(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            cost_per_request=round(cost_per_request, 6),
            cost_per_1k_requests=round(cost_per_1k, 4),
            estimated_monthly_cost=round(monthly_cost, 2),
            model_name=model_name,
            optimization_tips=tips
        )