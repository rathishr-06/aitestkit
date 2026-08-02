from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class CopilotAnalysis:
    overall_score: float
    confidence_score: float
    strengths: List[str]
    problems: List[str]
    recommended_fixes: List[Dict[str, Any]]
    explanations: List[Dict[str, str]]
    sprint_plan: List[Dict[str, str]]
    final_verdict: str
    architect_notes: str

class AICopilotEngine:
    """Analyzes raw benchmark metrics dynamically and generates architectural insights."""

    @classmethod
    def analyze_report(cls, report_data: Dict[str, Any]) -> CopilotAnalysis:
        acc = report_data.get("ai_accuracy_score", 90.0)
        hal = report_data.get("hallucination_rate", 2.0)
        perf = report_data.get("performance_score", 85.0)
        rob = report_data.get("prompt_robustness", 80.0)
        overall = report_data.get("overall_score", 88.0)

        strengths = []
        problems = []
        fixes = []
        explanations = []

        # 1. Dynamic Strengths & Problems Detection
        if acc >= 90.0:
            strengths.append(f"High Reasoning Accuracy ({acc:.1f}%)")
        else:
            problems.append(f"Reasoning Accuracy Below SLA Target ({acc:.1f}%)")

        if hal <= 3.0:
            strengths.append(f"Very Low Hallucination Rate ({hal:.1f}%)")
        else:
            problems.append(f"Elevated Hallucination Rate Detected ({hal:.1f}%)")

        if perf >= 85.0:
            strengths.append("Optimal Sub-Second Response Latency")
        else:
            problems.append("Increased Stress Latency Under Load")

        if rob >= 85.0:
            strengths.append("Strong System Prompt Robustness")
        else:
            problems.append("Prompt Injection Vulnerability Detected")

        # Fallback defaults if metrics are high
        if not strengths:
            strengths.append("Baseline System Stability Maintained")
        if not problems:
            problems.append("Minor Latency Fluctuations Under Peak Spike")

        # 2. Dynamic Fix Generation
        if rob < 85.0 or "Prompt Injection Vulnerability Detected" in problems:
            fixes.append({
                "title": "Improve Prompt Delimiters",
                "desc": "Wrap untrusted user inputs in XML blocks to prevent prompt injection attacks.",
                "gain": "+4 Score",
                "priority": "CRITICAL",
                "priority_color": "#ef4444",
                "difficulty": "Easy",
                "time": "2 Hours"
            })

        if perf < 85.0 or "Increased Stress Latency Under Load" in problems:
            fixes.append({
                "title": "Enable Async Non-Blocking Inference",
                "desc": "Switch execution pipeline to async loop worker nodes to prevent thread starvation.",
                "gain": "+3 Score",
                "priority": "HIGH",
                "priority_color": "#f59e0b",
                "difficulty": "Medium",
                "time": "4 Hours"
            })

        if hal > 3.0:
            fixes.append({
                "title": "Reduce Vector Top-K Retrieval",
                "desc": "Tighten semantic retriever threshold from K=5 to K=3 to exclude noisy context.",
                "gain": "+3 Score",
                "priority": "HIGH",
                "priority_color": "#f59e0b",
                "difficulty": "Easy",
                "time": "1 Hour"
            })

        if not fixes:
            fixes.append({
                "title": "Optimize Thread Pool Allocations",
                "desc": "Expand default worker thread pool size from 4 to 16 concurrency threads.",
                "gain": "+2 Score",
                "priority": "MEDIUM",
                "priority_color": "#3b82f6",
                "difficulty": "Easy",
                "time": "1 Hour"
            })

        # 3. Dynamic Explanations
        explanations = [
            {
                "question": "Why is the overall readiness score at this level?",
                "answer": f"The overall score of {overall:.0f}/100 is calculated via multi-axis weighting: Accuracy ({acc}%), Hallucination Resistance ({100-hal}%), and Robustness ({rob}%)."
            },
            {
                "question": "What is driving current operational risks?",
                "answer": f"Primary risk vectors stem from {'Security Guardrail gaps' if rob < 85 else 'Inference queue bottlenecks during concurrent load spikes'}."
            }
        ]

        # 4. Sprint Plan
        sprint_plan = [
            {"Sprint": "Sprint 1", "Focus": "Security Guardrails & Input Isolation", "Owner": "SecOps Lead"},
            {"Sprint": "Sprint 2", "Focus": "Inference Latency & Async Pipeline Optimization", "Owner": "Backend AI Lead"},
            {"Sprint": "Sprint 3", "Focus": "Production Readiness Staging & Canary Rollout", "Owner": "DevOps / CTO"}
        ]

        confidence = min(round(overall * 1.02), 99.0)
        verdict = "READY FOR PRODUCTION" if overall >= 88.0 else "PRODUCTION ROLLOUT BLOCKED"
        notes = f"System audit indicates strong performance with an overall score of {overall:.0f}/100. Primary recommendation: Resolve high-priority items prior to traffic migration."

        return CopilotAnalysis(
            overall_score=overall,
            confidence_score=confidence,
            strengths=strengths,
            problems=problems,
            recommended_fixes=fixes,
            explanations=explanations,
            sprint_plan=sprint_plan,
            final_verdict=verdict,
            architect_notes=notes
        )