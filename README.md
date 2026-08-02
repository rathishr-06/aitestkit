# ⚡ AITestKit — Enterprise SaaS & Open-Source AI Quality Control Engine

**AITestKit** is an end-to-end AI Quality Engineering & Production Readiness Framework. It provides automated benchmarking, hallucination tracking, prompt injection safety auditing, cost intelligence, and a dynamic **AI Quality Engineer Copilot**.

---

## 🚀 Key Features

* **🤖 AI Quality Engineer Copilot**: Architectural root-cause analysis, dynamic priority fix roadmaps, and interactive "What-If" score simulation.
* **🛡️ Security & Guardrails Audit**: Automated prompt injection, jailbreak, and PII leakage detection.
* **🧠 LLM & RAG Metrics Engine**: Semantic similarity, ground-truth faithfulness, accuracy, and hallucination scoring.
* **💰 Cost Intelligence & Token Analytics**: Granular token usage tracking, per-request cost attribution, and cloud bill forecasting.
* **⚡ Concurrency Load & Stress Tester**: P50/P90/P95 latency telemetry and memory drift auditing under heavy traffic.
* **🌐 SaaS REST Control Plane API**: FastAPI backend with SQLite persistence, multi-tenant authentication, async jobs, and webhook alerts.

---

## ⚙️ Installation

```bash
git clone [https://github.com/rathishr-06/aitestkit.git](https://github.com/rathishr-06/aitestkit.git)
cd aitestkit
python -m venv .venv
.venv\Scripts\activate   # On Windows
pip install -e .