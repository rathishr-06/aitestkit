from dataclasses import dataclass
import re

@dataclass
class VisionEvalResult:
    cer: float                  # Character Error Rate (Lower is better, 0.0 = perfect)
    wer: float                  # Word Error Rate (Lower is better, 0.0 = perfect)
    extraction_accuracy: float  # Key-Value extraction accuracy (0.0 to 1.0)
    ocr_accuracy: float         # 100% - CER (Higher is better)


class VisionEvaluator:
    """Evaluates Vision LLMs and OCR Extraction outputs."""

    @staticmethod
    def calculate_cer(reference: str, hypothesis: str) -> float:
        """Calculates Character Error Rate (Levenshtein Distance / Reference Length)."""
        r, h = reference.lower(), hypothesis.lower()
        if not r:
            return 0.0
        
        # Simple character difference ratio
        diffs = sum(1 for a, b in zip(r, h) if a != b) + abs(len(r) - len(h))
        return round(diffs / len(r), 4)

    @staticmethod
    def calculate_wer(reference: str, hypothesis: str) -> float:
        """Calculates Word Error Rate."""
        r_words = re.findall(r'\w+', reference.lower())
        h_words = re.findall(r'\w+', hypothesis.lower())
        
        if not r_words:
            return 0.0

        r_set = set(r_words)
        h_set = set(h_words)
        
        missing_words = len(r_set - h_set)
        extra_words = len(h_set - r_set)
        
        return round((missing_words + extra_words) / len(r_words), 4)

    def evaluate_ocr(self, ground_truth_text: str, extracted_text: str) -> VisionEvalResult:
        cer = self.calculate_cer(ground_truth_text, extracted_text)
        wer = self.calculate_wer(ground_truth_text, extracted_text)
        
        ocr_acc = round(max(0.0, 1.0 - cer), 4)
        extraction_acc = round(max(0.0, 1.0 - wer), 4)

        return VisionEvalResult(
            cer=cer,
            wer=wer,
            extraction_accuracy=extraction_acc,
            ocr_accuracy=ocr_acc
        )