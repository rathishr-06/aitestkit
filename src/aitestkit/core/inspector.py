import importlib.util
from typing import Dict, List

class FrameworkInspector:
    """Intelligent codebase and environment detector for AI projects."""

    FRAMEWORKS = {
        "LangChain": "langchain",
        "LlamaIndex": "llama_index",
        "OpenAI": "openai",
        "Anthropic": "anthropic",
        "Ollama": "ollama",
        "ChromaDB": "chromadb",
        "FAISS": "faiss",
        "Pinecone": "pinecone",
        "Milvus": "pymilvus",
    }

    @classmethod
    def scan_environment(cls) -> Dict[str, List[str]]:
        detected = []
        for name, module in cls.FRAMEWORKS.items():
            if importlib.util.find_spec(module) is not None:
                detected.append(name)
        
        recommendations = []
        if "ChromaDB" in detected or "FAISS" in detected or "Pinecone" in detected:
            recommendations.append("RAG Evaluation Module (eval-rag)")
        if "LangChain" in detected or "LlamaIndex" in detected:
            recommendations.append("Full Pipeline Security & Safety Audit (eval-safety)")
        if "Ollama" in detected:
            recommendations.append("Local Model Performance & TTFT Benchmark (load)")
        if "OpenAI" in detected or "Anthropic" in detected:
            recommendations.append("LLM Accuracy & Hallucination Benchmark (eval-llm)")

        return {
            "detected_stack": detected,
            "recommended_tests": recommendations if recommendations else ["Native Engine Tests"]
        }