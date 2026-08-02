from fastapi import FastAPI, HTTPException, Header, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uuid
import time

from aitestkit.core.readiness import ProductionReadinessEngine
from aitestkit.cost.calculator import CostIntelligenceEngine
from aitestkit.llm.metrics import LLMEvaluator
from aitestkit.safety.evaluator import SafetyEvaluator

app = FastAPI(
    title="AITestKit SaaS Control Plane API",
    description="Enterprise Multi-Tenant REST API for AI Quality Engineering & Production Readiness Certification.",
    version="1.0.0-SaaS"
)

# Mock Multi-Tenant API Key Database
API_KEY_DB = {
    "aitest_live_tenant_key_101": {"tenant_id": "org_fintech_corp", "tier": "enterprise"},
    "aitest_live_tenant_key_102": {"tenant_id": "org_healthcare_inc", "tier": "pro"}
}

def verify_tenant(x_api_key: str = Header(...)):
    """Tenant authentication dependency."""
    if x_api_key not in API_KEY_DB:
        raise HTTPException(status_code=401, detail="Invalid AITestKit SaaS API Key.")
    return API_KEY_DB[x_api_key]

# Request / Response Schemas
class EvalRequest(BaseModel):
    prompt: str
    response: str
    reference: Optional[str] = None
    model_name: Optional[str] = "gpt-4o-mini"
    prompt_tokens: Optional[int] = 150
    completion_tokens: Optional[int] = 80

class ReadinessRequest(BaseModel):
    domain: str = "Healthcare"
    performance_score: float = 95.0
    accuracy_score: float = 96.0
    hallucination_rate: float = 2.0
    robustness_score: float = 89.0

@app.get("/api/v1/health")
def health_check():
    return {"status": "online", "service": "AITestKit Control Plane API", "timestamp": time.time()}

@app.post("/api/v1/evaluate")
def evaluate_payload(req: EvalRequest, tenant: Dict[str, Any] = Depends(verify_tenant)):
    """Evaluate an LLM interaction and calculate cost telemetry."""
    llm_eval = LLMEvaluator().evaluate_response(req.prompt, req.response, req.reference or "")
    safety_eval = SafetyEvaluator().evaluate_safety(req.prompt + " " + req.response)
    cost_est = CostIntelligenceEngine.calculate_cost(req.prompt_tokens, req.completion_tokens, req.model_name)

    return {
        "evaluation_id": f"eval_{uuid.uuid4().hex[:8]}",
        "tenant_id": tenant["tenant_id"],
        "llm_metrics": llm_eval.__dict__,
        "safety_metrics": safety_eval.__dict__,
        "cost_telemetry": cost_est.__dict__
    }

@app.post("/api/v1/readiness")
def get_production_readiness(req: ReadinessRequest, tenant: Dict[str, Any] = Depends(verify_tenant)):
    """Get full production readiness score and deployment decision."""
    report = ProductionReadinessEngine.evaluate_readiness(
        perf_score=req.performance_score,
        accuracy_score=req.accuracy_score,
        hallucination_rate=req.hallucination_rate,
        robustness_score=req.robustness_score
    )
    return {
        "tenant_id": tenant["tenant_id"],
        "domain": req.domain,
        "readiness_report": report.__dict__
    }