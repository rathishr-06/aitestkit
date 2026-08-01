import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LLMEvalResult:
    accuracy_score: float         # 0.0 to 1.0
    semantic_similarity: float   # 0.0 to 1.0
    hallucination_score: float   # 0.0 to 1.0 (Higher = More Hallucination)
    completeness_score: float    # 0.0 to 1.0
    reasoning_quality: float     # 0.0 to 1.0


class LLMEvaluator:
    """Core evaluation engine for LLM outputs."""

    @staticmethod
    def _calculate_token_overlap(str1: str, str2: str) -> float:
        """Token-based Jaccard similarity index."""
        words1 = set(re.findall(r'\w+', str1.lower()))
        words2 = set(re.findall(r'\w+', str2.lower()))
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return round(len(intersection) / len(union), 4)

    def evaluate_response(
        self, 
        prompt: str, 
        generated_text: str, 
        reference_text: Optional[str] = None,
        context_facts: Optional[List[str]] = None
    ) -> LLMEvalResult:
        
        # 1. Semantic Similarity / Accuracy against Reference
        similarity = 0.0
        accuracy = 0.0
        if reference_text:
            similarity = self._calculate_token_overlap(generated_text, reference_text)
            accuracy = similarity  # Baseline token-match accuracy

        # 2. Hallucination Detection against Provided Context Facts
        hallucination_score = 0.0
        if context_facts:
            gen_words = set(re.findall(r'\w+', generated_text.lower()))
            unsupported_facts = 0
            
            for fact in context_facts:
                fact_words = set(re.findall(r'\w+', fact.lower()))
                if not fact_words.intersection(gen_words):
                    unsupported_facts += 1
            
            hallucination_score = round(unsupported_facts / len(context_facts), 4)

        # 3. Completeness (Ratio of output content to prompt requirements)
        gen_len = len(generated_text.split())
        completeness = min(1.0, round(gen_len / 20.0, 4)) # Standard heuristic threshold

        # 4. Reasoning Quality (Detects structured thinking steps like 'because', 'therefore', etc.)
        reasoning_keywords = ["because", "therefore", "step", "since", "so", "hence", "reason"]
        found_keywords = sum(1 for kw in reasoning_keywords if kw in generated_text.lower())
        reasoning_score = min(1.0, round(found_keywords / 3.0, 4))

        return LLMEvalResult(
            accuracy_score=accuracy,
            semantic_similarity=similarity,
            hallucination_score=hallucination_score,
            completeness_score=completeness,
            reasoning_quality=reasoning_score
        )