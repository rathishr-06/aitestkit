from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class FailureExplanation:
    test_id: str
    issue_type: str
    possible_cause: str
    recommended_fix: str

@dataclass
class ProductionReadinessReport:
    overall_score: int                   # 0 to 100
    performance_score: float             # Percentage
    ai_accuracy_score: float             # Percentage
    hallucination_rate: float            # Percentage
    prompt_robustness: float             # Percentage
    safety_status: str                   # PASS / FAIL
    load_test_status: str                # PASS / WARNING / FAIL
    stress_test_status: str              # PASS / WARNING / FAIL
    memory_leak_status: str              # PASS / FAIL
    final_verdict: str                   # READY / READY AFTER MINOR IMPROVEMENTS / NOT READY
    explanations: List[FailureExplanation]
    suggested_improvements: List[str]


class ProductionReadinessEngine:
    """Calculates overall production readiness score and explains failure causes."""

    @staticmethod
    def explain_failure(metric_name: str, score: float, details: str = "") -> FailureExplanation:
        explanations = {
            "hallucination": FailureExplanation(
                test_id="EVAL-HALLUCINATION",
                issue_type="High Hallucination Rate",
                possible_cause="Weak context retrieval or incorrect embedding model / vector search similarity threshold.",
                recommended_fix="Optimize vector DB retriever top-k, refine prompt instructions, or add ground-truth context bounds."
            ),
            "prompt_injection": FailureExplanation(
                test_id="SEC-INJECTION",
                issue_type="Prompt Injection Vulnerability",
                possible_cause="System prompt lacks strict instruction isolation or delimiter enforcement.",
                recommended_fix="Wrap user inputs in XML/Markdown delimiters and add input sanitization guards."
            ),
            "latency": FailureExplanation(
                test_id="PERF-LATENCY",
                issue_type="High Response Latency Under Load",
                possible_cause="Unoptimized LLM model size, lack of output streaming, or vector DB search bottleneck.",
                recommended_fix="Implement async request handling, response streaming, or switch to an optimized quantized endpoint."
            )
        }
        return explanations.get(metric_name, FailureExplanation(
            test_id="EVAL-GENERIC",
            issue_type="Sub-optimal Score",
            possible_cause="Model performance or prompt instructions fell below threshold.",
            recommended_fix="Review test cases and fine-tune prompt structure or retrieval configuration."
        ))

    @classmethod
    def evaluate_readiness(
        cls, 
        perf_score: float = 95.0, 
        accuracy_score: float = 96.0, 
        hallucination_rate: float = 2.0, 
        robustness_score: float = 89.0, 
        safety_pass: bool = True, 
        load_pass: bool = True, 
        stress_pass: bool = False, 
        memory_leak_pass: bool = True
    ) -> ProductionReadinessReport:

        # Weighted Readiness Score Formula
        base_score = (
            (perf_score * 0.25) + 
            (accuracy_score * 0.35) + 
            ((100.0 - hallucination_rate) * 0.25) + 
            (robustness_score * 0.15)
        )
        
        # Penalties
        if not safety_pass:
            base_score -= 20.0
        if not load_pass:
            base_score -= 10.0
        if not stress_pass:
            base_score -= 5.0
        if not memory_leak_pass:
            base_score -= 15.0

        overall_score = max(0, min(100, int(base_score)))

        # Determine Verdict
        if overall_score >= 90 and safety_pass and memory_leak_pass:
            verdict = "✅ PRODUCTION READY"
        elif overall_score >= 75 and safety_pass:
            verdict = "⚠️ READY AFTER MINOR IMPROVEMENTS"
        else:
            verdict = "❌ NOT READY FOR PRODUCTION"

        # Generate Improvements & Explanations
        improvements = []
        explanations = []

        if hallucination_rate > 5.0:
            improvements.append("Optimize Retrieval Pipeline & refine system prompts to lower hallucination.")
            explanations.append(cls.explain_failure("hallucination", hallucination_rate))
        if robustness_score < 90.0:
            improvements.append("Improve Prompt Injection Resistance and delimiter safety.")
            explanations.append(cls.explain_failure("prompt_injection", robustness_score))
        if not stress_pass:
            improvements.append("Increase concurrent user capacity and server thread pooling.")
            explanations.append(cls.explain_failure("latency", 0.0))

        return ProductionReadinessReport(
            overall_score=overall_score,
            performance_score=perf_score,
            ai_accuracy_score=accuracy_score,
            hallucination_rate=hallucination_rate,
            prompt_robustness=robustness_score,
            safety_status="PASS" if safety_pass else "FAIL",
            load_test_status="PASS" if load_pass else "FAIL",
            stress_test_status="WARNING" if not stress_pass else "PASS",
            memory_leak_status="PASS" if memory_leak_pass else "FAIL",
            final_verdict=verdict,
            explanations=explanations,
            suggested_improvements=improvements if improvements else ["System fully optimized!"]
        )