# AgentOps — Member Churn Prediction

> A production-grade multi-agent system for subscription churn prediction — streaming ingestion, XGBoost + LightGBM ensemble scoring, Claude-powered LLM explanation, and a self-improving memory layer.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What This Is

Most churn prediction systems stop at the model. This one doesn't.

This project implements a **two-layer multi-agent architecture**:

- **Static pipeline** — deterministic batch scoring: signal ingestion → feature engineering → XGBoost/LightGBM ensemble → SHAP explanation → personalized intervention
- **Dynamic layer** — LLM-powered reasoning: an OrchestratorAgent (CEO) routes tasks, a PersonalizationStrategistAgent decides *whether and how* to intervene, an ExperimentationAgent measures causal lift, and a MemoryAgent compounds learnings across every experiment

The result: a system that gets smarter after every intervention campaign, without anyone manually updating playbooks.

---

## Agent Architecture

```
OrchestratorAgent  (CEO — LLM-powered, entry point for all non-batch requests)
│
├── PersonalizationStrategistAgent
│   "Should we intervene? For whom, when, which channel, what offer?"
│
├── ChurnPredictionPipeline  (static, deterministic — runs on schedule)
│   ├── SignalIngestionAgent        real-time Kafka consumer + velocity detection
│   ├── FeatureBuilderAgent         40+ features, recency decay, Redis feature store
│   ├── RiskScorerAgent             XGBoost + LightGBM ensemble + SHAP
│   ├── LLMExplainerAgent           Claude API explanation + PII scrub + governance log
│   └── InterventionAgent           CRM router + suppression check + rate cap
│
├── ExperimentationAgent
│   "Is the intervention working? Measure causal lift via CUPED / DiD."
│
├── SyntheticDataAgent
│   "Generate training data. Simulate behavioral decay patterns."
│
└── MemoryAgent
    "What worked before? Write lessons. Seed future agent sessions."
```

**Build order matters**: specialist agents first (weeks 1–6), dynamic agents on top (weeks 7–10). An orchestrator with no agents beneath it is just prompt engineering with no output.

---

## Why This Architecture

**The model is not the hard problem.** XGBoost on churn has been solved. The hard problems are feature freshness, auditability, and the decision layer above the model.

**Feature freshness at scale.** A nightly batch job scores members on 24-hour-old signals. A member who opened the app this morning and closed after 8 seconds looks fine in last night's batch. The streaming architecture here keeps feature freshness under 90 seconds — the difference between *predicting* churn and *reacting* to it.

**The PersonalizationStrategistAgent is the missing layer.** Most churn programs treat all high-risk members identically. A 15% discount retains a price-sensitive member. The same offer trains a convenience-driven member to wait for discounts. The strategist agent scores 5 axes (customer value, business value, feasibility, confidence, strategic alignment) and decides whether to intervene at all — and if so, what form it takes. This is where most membership programs leave money on the table.

**Auditability is a product requirement.** Every agent writes to the audit log before passing output downstream. You can replay any pipeline run, debug any member's score, and pass a governance review without reverse-engineering model weights.

**The MemoryAgent is the compounding asset.** After 6 months of experiments, the system knows that free-shipping extensions retain the grocery-heavy segment at 2.3x the rate of discount offers. No team has this institutionalized. Most teams re-learn it every quarter. The MemoryAgent makes every future agent session smarter than the last.

**Explainability is what makes ops teams trust the model.** SHAP + Claude explanation turns a probability into a story an account manager can act on.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Agents | Python 3.10 · `BaseAgent` ABC · Pydantic schemas |
| ML | XGBoost · LightGBM · SHAP · scikit-learn |
| LLM | Anthropic Claude API (`claude-sonnet-4-6`) |
| Streaming | Kafka (Docker) · Redis feature store |
| API | FastAPI · Uvicorn · Swagger UI |
| Experimentation | CUPED variance reduction · statsmodels |
| Monitoring | Evidently · PSI drift detection · auto-retrain |
| CI | GitHub Actions · pytest · mypy |

---

## Quick Start

**Prerequisites:** Docker, Python 3.10+, Anthropic API key

```bash
# 1. Clone and set up environment
git clone https://github.com/reshshah/ds-coach.git
cd "ds-coach/projects/Personalization Famework"

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# 3. Start local infrastructure (Kafka + Redis)
docker-compose up -d

# 4. Generate synthetic member data (10k members, ~15% churn rate)
python data/synthetic/generate_members.py

# 5. Run the pipeline
python -m pipeline.churn_pipeline

# 6. Start the API server
uvicorn api.main:app --reload
# → Swagger UI at http://localhost:8000/docs
```

---

## Project Structure

```
├── agents/
│   ├── base_agent.py                    ← all agents inherit from here
│   ├── signal_ingestion/                ← Kafka consumer + velocity detection
│   ├── feature_builder/                 ← 40+ features + Redis feature store
│   ├── risk_scorer/                     ← XGBoost + LightGBM + SHAP + PSI drift
│   ├── llm_explainer/                   ← Claude API + PII scrub + governance log
│   ├── intervention/                    ← CRM router + suppression + rate cap
│   ├── personalization_strategist/      ← 5-axis scoring, gates intervention
│   ├── experimentation/                 ← CUPED lift + confounder detection
│   ├── orchestrator/                    ← LLM-powered CEO agent
│   └── memory/                          ← Redis knowledge base, TTL-managed
├── pipeline/
│   ├── churn_pipeline.py                ← static batch scoring orchestration
│   └── audit_log.py                     ← tamper-resistant agent audit trail
├── api/                                 ← FastAPI server + routes
├── data/synthetic/                      ← synthetic member behavioral data
├── monitoring/                          ← fairness checks + drift alerting
├── docs/
│   ├── architecture.md                  ← design decisions and tradeoffs
│   └── experiment-design.md             ← CUPED methodology + lift measurement
└── tests/
    ├── unit/                            ← per-agent unit tests
    └── integration/                     ← end-to-end pipeline tests
```

---

## 10-Week Build Sequence

| Week | What to build | Key decision |
|------|--------------|--------------|
| 1 | BaseAgent · audit log · Pydantic schemas · synthetic data | Foundation everything else depends on |
| 2 | SignalIngestionAgent + Kafka simulation | 7/14/30d rolling windows in Redis |
| 3 | FeatureBuilderAgent + feature store | 40+ features, recency decay, online serving |
| 4 | RiskScorerAgent + XGBoost + SHAP | PSI drift check, auto-retrain trigger |
| 5 | LLMExplainerAgent + Claude API + PII scrub | Governance log, bias audit |
| 6 | InterventionAgent + ChurnPredictionPipeline | Static pipeline end-to-end working |
| 7 | PersonalizationStrategistAgent | 5-axis scoring gates every intervention |
| 8 | ExperimentationAgent + CUPED lift | Causal measurement closes the loop |
| 9 | OrchestratorAgent (CEO) | LLM-powered routing across all agents |
| 10 | MemoryAgent + self-improvement loop | System compounds after every experiment |

Validate the static pipeline end-to-end before building the dynamic layer. The MemoryAgent is useless on day one and extremely valuable after 3 months of experiment results — plan for it architecturally from week 1.

---

## Key Design Decisions

- Agents are **stateless classes** inheriting `BaseAgent`; all state lives in Redis
- Every agent writes to `audit_log.py` **before** passing output downstream
- `PersonalizationStrategistAgent` must approve before `InterventionAgent` fires
- LLM explainer **always PII-scrubs** before calling Anthropic API
- Intervention rate capped at **15% of active members per day**
- Model auto-retrains when **PSI drift > 0.2**
- `MemoryAgent` key schema: `memory:{agent_name}:{topic}:{YYYY-MM-DD}`, TTL = 180 days

---

## Contributing

This project is structured so the agent framework is domain-agnostic. `BaseAgent`, the orchestrator pattern, the memory layer, and the audit log can all be adapted to any subscription churn problem — SaaS, media, fintech, healthcare.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new agent, extend the feature store, or plug in a different ML backend.

---

## License

MIT — use it, extend it, ship it.
