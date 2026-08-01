from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from aitestkit.llm.metrics import LLMEvaluator, LLMEvalResult
from aitestkit.rag.metrics import RAGEvaluator, RAGEvalResult
from aitestkit.safety.evaluator import SafetyEvaluator, SafetyEvalResult
from aitestkit.vision.evaluator import VisionEvaluator, VisionEvalResult
from aitestkit.reports.exporter import ReportExporter


@dataclass
class EvaluationSummary:
    llm: Optional[LLMEvalResult] = None
    rag: Optional[RAGEvalResult] = None
    safety: Optional[SafetyEvalResult] = None
    vision: Optional[VisionEvalResult] = None


class Evaluator:
    """Unified Orchestrator for AITestKit."""

    def __init__(self):
        self.llm_eval = LLMEvaluator()
        self.rag_eval = RAGEvaluator()
        self.safety_eval = SafetyEvaluator()
        self.vision_eval = VisionEvaluator()

    def run(
        self,
        prompt: Optional[str] = None,
        response: Optional[str] = None,
        reference: Optional[str] = None,
        contexts: Optional[List[str]] = None,
        ground_truth: Optional[str] = None,
        export_json_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Runs all relevant evaluation modules dynamically based on provided inputs."""
        summary = EvaluationSummary()
        result_dict = {}

        if prompt and response:
            summary.llm = self.llm_eval.evaluate_response(prompt, response, reference, contexts)
            summary.safety = self.safety_eval.evaluate_safety(f"{prompt} {response}")
            result_dict["llm"] = asdict(summary.llm)
            result_dict["safety"] = asdict(summary.safety)

        if prompt and response and contexts:
            summary.rag = self.rag_eval.evaluate_rag(prompt, response, contexts, ground_truth)
            result_dict["rag"] = asdict(summary.rag)

        if reference and response and not prompt:
            summary.vision = self.vision_eval.evaluate_ocr(reference, response)
            result_dict["vision"] = asdict(summary.vision)

        if export_json_path:
            ReportExporter.export_json(result_dict, export_json_path)

        return result_dict