import re
from dataclasses import dataclass
from typing import List

@dataclass
class RAGEvalResult:
    faithfulness: float         # 0.0 to 1.0
    answer_relevance: float     # 0.0 to 1.0
    context_relevance: float    # 0.0 to 1.0
    context_recall: float       # 0.0 to 1.0
    context_precision: float    # 0.0 to 1.0

class RAGEvaluator:
    """Core evaluation engine for RAG pipelines."""

    @staticmethod
    def _token_set(text: str) -> set[str]:
        return set(re.findall(r'\w+', text.lower()))

    def evaluate_rag(
        self,
        query: str,
        response: str,
        contexts: List[str],
        ground_truth: str = None
    ) -> RAGEvalResult:
        query_tokens = self._token_set(query)
        response_tokens = self._token_set(response)
        
        combined_context = " ".join(contexts)
        context_tokens = self._token_set(combined_context)

        # 1. Faithfulness (How much of response is grounded in context)
        if response_tokens:
            faithful_tokens = response_tokens.intersection(context_tokens)
            faithfulness = round(len(faithful_tokens) / len(response_tokens), 4)
        else:
            faithfulness = 0.0

        # 2. Answer Relevance (Overlap between Query and Response tokens)
        if query_tokens and response_tokens:
            relevant_tokens = query_tokens.intersection(response_tokens)
            answer_relevance = round(len(relevant_tokens) / len(query_tokens), 4)
        else:
            answer_relevance = 0.0

        # 3. Context Relevance (Overlap between Query and Contexts)
        if query_tokens and context_tokens:
            ctx_rel_tokens = query_tokens.intersection(context_tokens)
            context_relevance = round(len(ctx_rel_tokens) / len(query_tokens), 4)
        else:
            context_relevance = 0.0

        # 4. Context Recall & Precision (Compared against Ground Truth if present)
        context_recall = 0.0
        context_precision = 0.0
        if ground_truth:
            gt_tokens = self._token_set(ground_truth)
            if gt_tokens:
                retained = gt_tokens.intersection(context_tokens)
                context_recall = round(len(retained) / len(gt_tokens), 4)
                context_precision = round(len(retained) / len(context_tokens), 4) if context_tokens else 0.0

        return RAGEvalResult(
            faithfulness=faithfulness,
            answer_relevance=answer_relevance,
            context_relevance=context_relevance,
            context_recall=context_recall,
            context_precision=context_precision
        )