from typing import Optional, Dict, Any
from aitestkit.llm.metrics import LLMEvaluator
from aitestkit.safety.evaluator import SafetyEvaluator
from aitestkit.cost.calculator import CostIntelligenceEngine
from aitestkit.core.readiness import ProductionReadinessEngine

class AITestKit:
    """
    Open-Source One-Click AI Evaluation Engine.
    Runs Accuracy, Hallucination, Security Audit, Cost Telemetry,
    and Production Readiness Scoring in a single call.
    """
    def __init__(self, project_name: str = "AI-Application"):
        self.project_name = project_name
        self.llm_evaluator = LLMEvaluator()
        self.safety_evaluator = SafetyEvaluator()

    def run_full_test(
        self,
        prompt: str,
        response: str,
        reference: str = "",
        model_name: str = "gpt-4o-mini",
        prompt_tokens: int = 150,
        completion_tokens: int = 80
    ) -> Dict[str, Any]:
        """Executes full evaluation suite in ONE SINGLE CLICK / CALL."""
        
        # 1. LLM Evaluation (Accuracy & Hallucination)
        llm_res = self.llm_evaluator.evaluate_response(prompt, response, reference)
        
        # 2. Safety Audit (Prompt Injection & Risk)
        safety_res = self.safety_evaluator.evaluate_safety(prompt + " " + response)
        
        # 3. Cost Telemetry
        cost_res = CostIntelligenceEngine.calculate_cost(prompt_tokens, completion_tokens, model_name)
        
        # 4. Production Readiness Calculation
        readiness_report = ProductionReadinessEngine.evaluate_readiness(
            accuracy_score=llm_res.accuracy_score * 100,
            hallucination_rate=llm_res.hallucination_score * 100,
            robustness_score=90.0 if safety_res.is_safe else 50.0
        )

        return {
            "project_name": self.project_name,
            "readiness_score": readiness_report.overall_score,
            "verdict": readiness_report.final_verdict,
            "is_safe": safety_res.is_safe,
            "accuracy": f"{llm_res.accuracy_score * 100:.1f}%",
            "hallucination": f"{llm_res.hallucination_score * 100:.1f}%",
            "cost_per_request": f"${cost_res.cost_per_request:.6f}",
            "full_details": {
                "llm_metrics": llm_res.__dict__,
                "safety_metrics": safety_res.__dict__,
                "cost_telemetry": cost_res.__dict__,
                "readiness_report": readiness_report.__dict__
            }
        }