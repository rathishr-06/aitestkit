from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class ModelBenchmarkEntry:
    model_name: str
    accuracy: float            # 0.0 to 100.0%
    latency_sec: float         # Lower is better
    throughput_tps: float      # Tokens per second (Higher is better)
    safety_score: float        # 0.0 to 100.0%
    overall_score: float       # Aggregated score


class LeaderboardEngine:
    """Ranks and compares multiple LLM models/endpoints based on performance & quality."""

    def calculate_score(self, accuracy: float, latency: float, tps: float, safety: float) -> float:
        # Weighted metric scoring formula
        latency_score = max(0.0, 100.0 - (latency * 20.0))  # Penalty for higher latency
        tps_score = min(100.0, tps * 2.0)
        
        weighted_score = (
            (accuracy * 0.35) + 
            (safety * 0.25) + 
            (latency_score * 0.20) + 
            (tps_score * 0.20)
        )
        return round(weighted_score, 2)

    def rank_models(self, entries: List[Dict[str, Any]]) -> List[ModelBenchmarkEntry]:
        ranked_list = []
        for entry in entries:
            score = self.calculate_score(
                entry.get("accuracy", 0.0),
                entry.get("latency_sec", 1.0),
                entry.get("throughput_tps", 0.0),
                entry.get("safety_score", 100.0)
            )
            ranked_list.append(ModelBenchmarkEntry(
                model_name=entry["model_name"],
                accuracy=entry.get("accuracy", 0.0),
                latency_sec=entry.get("latency_sec", 0.0),
                throughput_tps=entry.get("throughput_tps", 0.0),
                safety_score=entry.get("safety_score", 100.0),
                overall_score=score
            ))

        # Sort by overall score descending
        ranked_list.sort(key=lambda x: x.overall_score, reverse=True)
        return ranked_list