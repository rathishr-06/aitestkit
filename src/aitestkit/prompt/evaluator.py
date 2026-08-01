from dataclasses import dataclass

@dataclass
class PromptEvalResult:
    quality_score: float      # 0.0 to 1.0
    robustness_score: float   # 0.0 to 1.0
    format_validity: float    # 0.0 to 1.0

class PromptEvaluator:
    """Evaluates prompt structure and model output formatting adherence."""

    def evaluate_prompt(self, prompt: str, response: str, expected_format: str = "text") -> PromptEvalResult:
        words = prompt.split()
        quality_score = min(1.0, round(len(words) / 10.0, 2))

        format_valid = 1.0
        if expected_format.lower() == "json":
            import json
            try:
                json.loads(response)
                format_valid = 1.0
            except Exception:
                format_valid = 0.0

        robustness = round((quality_score + format_valid) / 2.0, 2)

        return PromptEvalResult(
            quality_score=quality_score,
            robustness_score=robustness,
            format_validity=format_valid
        )