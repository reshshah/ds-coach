# AgentOps: Member Churn Prediction — Project Setup Guide

**Stack:** Claude Code · VS Code · GitHub · Python · FastAPI · Kafka (simulated) · Redis · Vertex AI (target)

---

## Agent Architecture Overview

This system uses a two-layer agent design. The static pipeline handles deterministic batch scoring. The dynamic orchestrator layer handles reasoning, delegation, and self-improvement.

```
OrchestratorAgent  (CEO — LLM-powered, entry point for all non-batch requests)
│
├── PersonalizationStrategistAgent
│   "Should we intervene? For whom, when, which channel, what offer?"
│
├── ChurnPredictionPipeline  (static, deterministic — runs on schedule)
│   ├── SignalIngestionAgent        Wk 2
│   ├── FeatureBuilderAgent         Wk 3
│   ├── RiskScorerAgent             Wk 4
│   ├── LLMExplainerAgent           Wk 5
│   └── InterventionAgent           Wk 6
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

Build order matters: specialist agents first (weeks 1–6), dynamic agents on top (weeks 7–10). An orchestrator coordinating agents that do not exist yet is just prompt engineering with no output.

---

## Phase 0 — Prerequisites

Before touching code, verify these are installed:

```bash
node --version        # need v18+
python --version      # need 3.10+
git --version         # any recent version
docker --version      # for local Kafka/Redis simulation
```

Install Claude Code CLI:

```bash
npm install -g @anthropic-ai/claude-code
```

Install the VS Code extension: open VS Code → Extensions panel → search "Claude Code" by Anthropic (verified publisher, ⚡ Spark icon). The CLI and extension work together — the CLI runs in terminal, the extension gives you diff review and Problems panel integration.

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# Add to ~/.zshrc or ~/.bashrc to persist
```

---

## Phase 1 — GitHub Repository Setup

### 1.1 Create the repo

```bash
# On GitHub: New repo → name: agentops-churn-prediction
# Check: Add README, .gitignore (Python), MIT License

git clone https://github.com/YOUR_USERNAME/agentops-churn-prediction.git
cd agentops-churn-prediction
```

### 1.2 Branch strategy

```
main          ← production-ready, protected
├── develop   ← integration branch
│   ├── feature/signal-ingestion-agent
│   ├── feature/feature-builder-agent
│   ├── feature/risk-scorer-agent
│   ├── feature/llm-explainer-agent
│   ├── feature/intervention-agent
│   ├── feature/personalization-strategist-agent
│   ├── feature/experimentation-agent
│   ├── feature/orchestrator-agent
│   └── feature/memory-agent
```

```bash
git checkout -b develop
git push -u origin develop
```

### 1.3 Protect main branch (GitHub UI)

Settings → Branches → Add rule → `main` → require PR + 1 review + status checks.

---

## Phase 2 — VS Code Workspace Setup

### 2.1 Open in VS Code

```bash
code .
```

### 2.2 Recommended extensions (install all)

- Python (Microsoft)
- Pylance
- Claude Code (Anthropic) — already done
- GitLens
- Docker
- Jupyter

### 2.3 Create `.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "files.exclude": { "**/__pycache__": true, "**/.pytest_cache": true }
}
```

---

## Phase 3 — Project Structure

```
agentops-churn-prediction/
├── CLAUDE.md                              ← Claude Code project context (critical)
├── README.md
├── requirements.txt
├── docker-compose.yml                     ← local Kafka + Redis
├── .env.example
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py                      ← shared Agent base class
│   │
│   ├── signal_ingestion/                  ← Wk 2
│   │   ├── agent.py
│   │   ├── kafka_consumer.py
│   │   └── velocity_detector.py
│   │
│   ├── feature_builder/                   ← Wk 3
│   │   ├── agent.py
│   │   ├── feature_store.py
│   │   └── features.py                    ← 40+ feature definitions
│   │
│   ├── risk_scorer/                       ← Wk 4
│   │   ├── agent.py
│   │   ├── model.py                       ← XGBoost + LightGBM ensemble
│   │   ├── drift_detector.py              ← PSI / KL divergence
│   │   └── shap_explainer.py
│   │
│   ├── llm_explainer/                     ← Wk 5
│   │   ├── agent.py
│   │   ├── claude_client.py               ← Anthropic API calls
│   │   ├── pii_scrubber.py
│   │   └── governance_logger.py
│   │
│   ├── intervention/                      ← Wk 6
│   │   ├── agent.py
│   │   ├── crm_router.py
│   │   └── suppression_check.py
│   │
│   ├── personalization_strategist/        ← Wk 7
│   │   ├── agent.py                       ← WHO / WHAT / WHEN / WHERE / HOW MUCH
│   │   ├── decision_engine.py             ← opportunity scoring (1-10 per axis)
│   │   ├── channel_selector.py            ← email / push / SMS / web / app
│   │   └── guardrails.py                  ← do-not-personalize rules
│   │
│   ├── experimentation/                   ← Wk 8
│   │   ├── agent.py
│   │   ├── experiment_designer.py         ← hypothesis, sample size, duration
│   │   ├── cuped.py                       ← variance reduction
│   │   ├── lift_calculator.py             ← incremental revenue / retention
│   │   └── confound_detector.py
│   │
│   ├── orchestrator/                      ← Wk 9
│   │   ├── agent.py                       ← LLM-powered CEO agent
│   │   ├── task_router.py                 ← which agents to activate
│   │   └── executive_summary.py           ← output format for stakeholders
│   │
│   └── memory/                            ← Wk 10
│       ├── agent.py
│       ├── knowledge_store.py             ← Redis + structured JSON
│       ├── lesson_writer.py               ← writes after every experiment
│       └── lesson_reader.py               ← seeds agent sessions with prior learnings
│
├── data/
│   ├── synthetic/
│   │   ├── generate_members.py            ← synthetic member behavior
│   │   └── seed_data.py
│   └── schemas/
│       └── member_event.py                ← Pydantic schemas
│
├── pipeline/
│   ├── churn_pipeline.py                  ← static deterministic pipeline (batch)
│   ├── audit_log.py                       ← tamper-resistant logging
│   └── health_check.py
│
├── api/
│   ├── main.py                            ← FastAPI server
│   ├── routes/
│   │   ├── members.py
│   │   ├── pipeline.py
│   │   ├── orchestrator.py                ← CEO agent API endpoint
│   │   └── audit.py
│   └── models.py
│
├── monitoring/
│   ├── fairness.py                        ← demographic parity checks
│   ├── drift_monitor.py
│   └── alerting.py
│
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## Phase 4 — CLAUDE.md (The Most Important File)

This file is what makes Claude Code useful. It gives Claude persistent context about your project at the start of every session. Put it in your project root and keep it updated as the architecture evolves.

```markdown
# AgentOps — Member Churn Prediction

## What this project does
Predicts RetainIQ member intent-to-churn 30-60 days before cancellation using
real-time behavioral signals, an XGBoost/LightGBM ensemble, and a Claude-powered
LLM explanation layer. Ten agents operate across two layers:
- Static pipeline: deterministic batch scoring (signal → feature → score → explain → intervene)
- Dynamic layer: LLM-powered reasoning, strategy, experimentation, and memory

## Agent hierarchy
OrchestratorAgent is the entry point for all non-batch requests.
It uses Claude to reason about the task and decide which agents to activate.

PersonalizationStrategistAgent runs BEFORE InterventionAgent.
It scores the intervention opportunity and decides:
should we personalize (yes/no), what channel, what offer type, what timing.
Output is a PersonalizationDecision object with a priority score (1-10 per axis).

ExperimentationAgent runs AFTER interventions have been delivered.
It measures causal lift (CUPED / DiD) and writes results to MemoryAgent.

MemoryAgent is a read/write knowledge base (Redis + structured JSON).
Every agent reads from memory at session start before generating recommendations.
Every agent writes lessons learned after task completion.
Memory compounds: the system gets smarter after every experiment.

The static ChurnPredictionPipeline (pipeline/churn_pipeline.py) handles batch
scoring only. The OrchestratorAgent handles everything else.

## Architecture decisions
- Agents are stateless classes inheriting BaseAgent; state lives in Redis
- All agent outputs are written to audit_log.py before downstream routing
- LLM explainer always PII-scrubs before calling Anthropic API
- PersonalizationStrategistAgent must approve before InterventionAgent routes
- Intervention rate is capped at 15% of active members per day (guardrails.py)
- Model retrains automatically when PSI drift > 0.2 (drift_detector.py)
- MemoryAgent knowledge base key schema: memory:{agent_name}:{topic}:{date}

## Personalization decision axes (PersonalizationStrategistAgent)
Score each axis 1-10. Only proceed if total score >= 30/50.
- Customer Value: does this member benefit from the intervention?
- Business Value: what is the estimated incremental revenue lift?
- Technical Feasibility: is the data quality sufficient?
- Confidence Level: how certain are we of the churn signal?
- Strategic Alignment: does this fit RetainIQ membership growth goals?

## Code conventions
- Python 3.10+, type hints everywhere, Pydantic for all schemas
- Black formatting, isort imports, mypy strict mode
- Each agent has its own test file in tests/unit/
- Never hardcode API keys; use .env via python-dotenv
- Commit messages: feat/fix/refactor/test/docs prefix

## Key files to understand first
- agents/base_agent.py — all agents inherit from here
- pipeline/churn_pipeline.py — static batch scoring pipeline
- agents/orchestrator/agent.py — CEO agent, dynamic routing
- agents/memory/knowledge_store.py — shared knowledge base
- data/schemas/member_event.py — the core data contract

## What NOT to do
- Do not put business logic in api/routes/ — it belongs in agents/
- Do not call Anthropic API without going through llm_explainer/claude_client.py
- Do not skip the PII scrubber before any LLM call
- Do not call InterventionAgent without PersonalizationStrategistAgent approval
- Do not write to MemoryAgent without also logging to audit_log.py
- Do not modify main branch directly; always use a feature branch
```

---

## Phase 5 — Environment Setup

### 5.1 Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### 5.2 `requirements.txt`

```
# Core
fastapi==0.111.0
uvicorn[standard]==0.30.0
pydantic==2.7.0
python-dotenv==1.0.1

# ML
xgboost==2.0.3
lightgbm==4.3.0
scikit-learn==1.5.0
shap==0.45.0
numpy==1.26.4
pandas==2.2.2

# Anthropic
anthropic==0.28.0

# Streaming simulation
redis==5.0.4
kafka-python==2.0.2
faker==25.2.0

# Monitoring + experimentation
scipy==1.13.0
evidently==0.4.30
statsmodels==0.14.2

# Testing
pytest==8.2.0
pytest-asyncio==0.23.7
httpx==0.27.0
```

### 5.3 `.env.example` (commit this; never commit `.env`)

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
REDIS_URL=redis://localhost:6379
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
ENVIRONMENT=development
INTERVENTION_RATE_CAP=0.15
CHURN_SCORE_THRESHOLD=0.65
PSI_DRIFT_THRESHOLD=0.2
PERSONALIZATION_MIN_SCORE=30
MEMORY_TTL_DAYS=180
```

### 5.4 `docker-compose.yml` for local infrastructure

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  zookeeper:
    image: confluentinc/cp-zookeeper:7.6.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.6.0
    depends_on: [zookeeper]
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
```

```bash
docker-compose up -d
```

---

## Phase 6 — Base Agent

Everything inherits from this. Build it first.

```python
# agents/base_agent.py
import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from pipeline.audit_log import AuditLog

logger = logging.getLogger(__name__)

@dataclass
class AgentResult:
    agent_name: str
    success: bool
    output: Any
    duration_ms: float
    metadata: dict = field(default_factory=dict)
    error: str | None = None

class BaseAgent(ABC):
    """All AgentOps agents inherit from this class."""

    def __init__(self, name: str):
        self.name = name
        self.audit = AuditLog()

    def run(self, payload: dict) -> AgentResult:
        start = time.perf_counter()
        self.audit.log(agent=self.name, event="started", payload_keys=list(payload.keys()))
        try:
            output = self.execute(payload)
            duration = (time.perf_counter() - start) * 1000
            self.audit.log(agent=self.name, event="completed", duration_ms=round(duration))
            return AgentResult(
                agent_name=self.name,
                success=True,
                output=output,
                duration_ms=round(duration),
            )
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            self.audit.log(agent=self.name, event="error", error=str(e))
            logger.error(f"[{self.name}] failed: {e}", exc_info=True)
            return AgentResult(
                agent_name=self.name,
                success=False,
                output=None,
                duration_ms=round(duration),
                error=str(e),
            )

    @abstractmethod
    def execute(self, payload: dict) -> Any:
        """Implement agent logic here."""
        ...

    def health_check(self) -> bool:
        return True
```

---

## Phase 7 — Synthetic Data Generator

Run this before any agent development. All agents need data to run against.

```python
# data/synthetic/generate_members.py
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime

fake = Faker()
np.random.seed(42)

def generate_member_cohort(n: int = 10_000) -> pd.DataFrame:
    """
    Generate synthetic RetainIQ member behavioral data.
    Churn signal embedded in behavioral decay patterns.
    """
    now = datetime.utcnow()
    records = []

    for _ in range(n):
        will_churn = np.random.random() < 0.15
        decay = np.random.uniform(0.3, 0.8) if will_churn else np.random.uniform(0.85, 1.1)
        baseline_app_opens = np.random.poisson(lam=12)

        records.append({
            "member_id": f"M-{fake.unique.random_int(min=10000, max=99999)}",
            "tenure_days": np.random.randint(30, 1200),
            "renewal_days_remaining": np.random.randint(1, 90),
            "segment": np.random.choice(["grocery_heavy", "convenience", "price_sensitive", "mixed"]),

            # Behavioral signals — decayed for churners
            "app_opens_7d": max(0, int(baseline_app_opens * decay + np.random.normal(0, 1))),
            "app_opens_30d_baseline": baseline_app_opens * 4,
            "basket_refill_rate": round(np.clip(np.random.normal(0.7, 0.15) * decay, 0, 1), 3),
            "session_duration_minutes": round(max(0, np.random.exponential(8) * decay), 1),
            "free_shipping_utilization": round(np.clip(np.random.normal(0.6, 0.2), 0, 1), 3),
            "nudge_skips_30d": np.random.choice([0,1,2,3,4], p=[0.5,0.2,0.15,0.1,0.05])
                               if will_churn else np.random.choice([0,1], p=[0.85,0.15]),
            "category_breadth": max(1, int(np.random.normal(5, 2) * (1 if not will_churn else decay))),
            "pickup_to_delivery_shift": round(np.random.uniform(0, 0.4) * (2 if will_churn else 1), 3),

            # Ground truth — training only, never passed to model at inference
            "churned_within_60d": int(will_churn),
            "generated_at": now.isoformat(),
        })

    return pd.DataFrame(records)

if __name__ == "__main__":
    df = generate_member_cohort(10_000)
    df.to_csv("data/synthetic/members.csv", index=False)
    print(f"Generated {len(df)} members. Churn rate: {df.churned_within_60d.mean():.1%}")
```

---

## Phase 8 — New Agent Skeletons (Weeks 7–10)

### PersonalizationStrategistAgent

```python
# agents/personalization_strategist/agent.py
from dataclasses import dataclass
from agents.base_agent import BaseAgent, AgentResult
from agents.memory.agent import MemoryAgent

@dataclass
class PersonalizationDecision:
    member_id: str
    should_personalize: bool
    channel: str           # email | push | sms | web | app
    offer_type: str        # discount | free_ship_extension | loyalty_points | none
    timing: str            # immediate | daily | weekly | triggered
    priority_score: float  # 0-50 composite across 5 axes
    rationale: str

SCORE_THRESHOLD = 30  # from .env: PERSONALIZATION_MIN_SCORE

class PersonalizationStrategistAgent(BaseAgent):
    """
    Decides WHO gets personalization, WHAT type, WHEN, WHERE, and HOW MUCH.
    Runs before InterventionAgent. If priority_score < threshold, no intervention.
    Reads MemoryAgent for prior experiment results on similar segments.
    """

    def __init__(self):
        super().__init__("PersonalizationStrategistAgent")
        self.memory = MemoryAgent()

    def execute(self, payload: dict) -> dict:
        member = payload["member"]
        churn_score = payload["churn_score"]
        shap_top_features = payload["shap_features"]

        # Read prior learnings for this segment
        prior = self.memory.read(topic="intervention_outcomes", segment=member["segment"])

        # Score each axis 1-10
        customer_value   = self._score_customer_value(member, churn_score)
        business_value   = self._score_business_value(member, prior)
        feasibility      = self._score_feasibility(payload)
        confidence       = self._score_confidence(churn_score, shap_top_features)
        strategic_align  = self._score_strategic_alignment(member)

        total = customer_value + business_value + feasibility + confidence + strategic_align

        should_personalize = total >= SCORE_THRESHOLD

        decision = PersonalizationDecision(
            member_id=member["member_id"],
            should_personalize=should_personalize,
            channel=self._select_channel(member, prior),
            offer_type=self._select_offer(member, shap_top_features, prior),
            timing=self._select_timing(member),
            priority_score=total,
            rationale=self._build_rationale(
                customer_value, business_value, feasibility, confidence, strategic_align, prior
            ),
        )

        self.audit.log(
            agent=self.name,
            event="decision",
            member_id=member["member_id"],
            should_personalize=should_personalize,
            priority_score=total,
        )

        return {"personalization_decision": decision.__dict__}

    def _score_customer_value(self, member: dict, churn_score: float) -> float:
        # High tenure + high churn score = high customer value to retain
        tenure_score = min(10, member["tenure_days"] / 120)
        return round((churn_score * 5) + (tenure_score * 0.5), 1)

    def _score_business_value(self, member: dict, prior: dict) -> float:
        # Use prior experiment lift for this segment if available
        if prior and "avg_revenue_lift" in prior:
            return min(10, prior["avg_revenue_lift"] * 10)
        return 5.0  # default when no prior data

    def _score_feasibility(self, payload: dict) -> float:
        # Check data quality — all required features present and non-null
        required = ["app_opens_7d", "basket_refill_rate", "nudge_skips_30d"]
        present = all(payload["member"].get(f) is not None for f in required)
        return 9.0 if present else 4.0

    def _score_confidence(self, churn_score: float, shap_features: list) -> float:
        # High score + concentrated SHAP (one dominant feature) = high confidence
        if not shap_features:
            return 4.0
        top_shap = shap_features[0]["value"]
        return round(min(10, churn_score * 7 + top_shap * 3), 1)

    def _score_strategic_alignment(self, member: dict) -> float:
        # Grocery-heavy and convenience segments are highest RetainIQ priority
        alignment_map = {"grocery_heavy": 9, "convenience": 8, "price_sensitive": 6, "mixed": 7}
        return alignment_map.get(member.get("segment", "mixed"), 7)

    def _select_channel(self, member: dict, prior: dict) -> str:
        if prior and "best_channel" in prior:
            return prior["best_channel"]
        return "email"  # default

    def _select_offer(self, member: dict, shap_features: list, prior: dict) -> str:
        if prior and "best_offer" in prior:
            return prior["best_offer"]
        top_signal = shap_features[0]["feature"] if shap_features else ""
        if "free_shipping" in top_signal:
            return "free_ship_extension"
        if member.get("segment") == "price_sensitive":
            return "discount"
        return "loyalty_points"

    def _select_timing(self, member: dict) -> str:
        days = member.get("renewal_days_remaining", 30)
        if days <= 7:
            return "immediate"
        if days <= 14:
            return "daily"
        return "weekly"

    def _build_rationale(self, cv, bv, f, c, sa, prior) -> str:
        return (
            f"Scores — customer value: {cv}, business value: {bv}, "
            f"feasibility: {f}, confidence: {c}, strategic alignment: {sa}. "
            f"Prior data: {'available' if prior else 'none'}."
        )
```

### OrchestratorAgent (CEO)

```python
# agents/orchestrator/agent.py
import anthropic
from agents.base_agent import BaseAgent
from agents.memory.agent import MemoryAgent
from pipeline.churn_pipeline import ChurnPredictionPipeline

SYSTEM_PROMPT = """
You are the OrchestratorAgent for a RetainIQ Member Churn Prediction system.

Your responsibility is to coordinate all agents and maximize member retention
and incremental business value.

Available agents:
- ChurnPredictionPipeline: deterministic batch scoring (signal → feature → score → explain → intervene)
- PersonalizationStrategistAgent: decides intervention strategy per member
- ExperimentationAgent: designs and measures A/B tests and causal lift
- SyntheticDataAgent: generates training data and simulations
- MemoryAgent: reads/writes experiment learnings and prior outcomes

For every request:
1. Understand the business problem.
2. Check memory for relevant prior learnings.
3. Create an execution plan — which agents to activate and in what order.
4. Review all outputs.
5. Decide: proceed / iterate / reject.

Output format:
# Executive Summary
## Business Goal
## Agents Activated
## Decisions
## Risks
## Next Actions

Think like a Chief Analytics Officer balancing customer experience,
retention, incrementality, and engineering effort.
"""

class OrchestratorAgent(BaseAgent):
    """
    LLM-powered CEO agent. Entry point for all non-batch requests.
    Uses Claude to reason about the task and delegate to specialist agents.
    """

    def __init__(self):
        super().__init__("OrchestratorAgent")
        self.client = anthropic.Anthropic()
        self.memory = MemoryAgent()
        self.pipeline = ChurnPredictionPipeline()

    def execute(self, payload: dict) -> dict:
        task = payload.get("task", "")
        context = payload.get("context", {})

        # Seed with memory before reasoning
        prior_learnings = self.memory.read(topic="orchestrator_decisions")

        messages = [
            {
                "role": "user",
                "content": (
                    f"Task: {task}\n\n"
                    f"Context: {context}\n\n"
                    f"Prior learnings from memory:\n{prior_learnings}"
                ),
            }
        ]

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages,
        )

        plan = response.content[0].text

        # Parse plan and activate agents (implement routing logic here)
        activated = self._route(plan, payload)

        # Write decision to memory for future sessions
        self.memory.write(
            topic="orchestrator_decisions",
            content={"task": task, "plan_summary": plan[:200], "agents_activated": activated},
        )

        return {"plan": plan, "agents_activated": activated}

    def _route(self, plan: str, payload: dict) -> list[str]:
        """Simple keyword routing — replace with structured output parsing."""
        activated = []
        if "pipeline" in plan.lower() or "score" in plan.lower():
            self.pipeline.run(payload)
            activated.append("ChurnPredictionPipeline")
        if "experiment" in plan.lower():
            activated.append("ExperimentationAgent")
        return activated
```

### MemoryAgent

```python
# agents/memory/agent.py
import json
import redis
import os
from datetime import datetime
from agents.base_agent import BaseAgent

class MemoryAgent(BaseAgent):
    """
    Read/write knowledge base shared across all agents.
    Key schema: memory:{agent_name}:{topic}:{YYYY-MM-DD}
    Agents read from memory before generating recommendations.
    Agents write lessons learned after task completion.
    """

    def __init__(self):
        super().__init__("MemoryAgent")
        self.redis = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        self.ttl_days = int(os.getenv("MEMORY_TTL_DAYS", 180))

    def execute(self, payload: dict) -> dict:
        op = payload.get("operation")
        if op == "read":
            return {"result": self.read(payload.get("topic"), payload.get("segment"))}
        if op == "write":
            self.write(payload.get("topic"), payload.get("content"), payload.get("agent"))
            return {"result": "written"}
        return {"result": None}

    def read(self, topic: str, segment: str = None, agent: str = "*") -> dict | None:
        """Search memory for relevant prior learnings on a topic."""
        pattern = f"memory:{agent}:{topic}:*"
        keys = self.redis.keys(pattern)
        if not keys:
            return None
        # Return most recent entry
        latest_key = sorted(keys)[-1]
        raw = self.redis.get(latest_key)
        if not raw:
            return None
        data = json.loads(raw)
        if segment and data.get("segment") and data["segment"] != segment:
            return None
        return data

    def write(self, topic: str, content: dict, agent: str = "system") -> None:
        """Write a lesson learned to the knowledge base."""
        key = f"memory:{agent}:{topic}:{datetime.utcnow().strftime('%Y-%m-%d')}"
        self.redis.setex(
            key,
            self.ttl_days * 86400,
            json.dumps({**content, "written_at": datetime.utcnow().isoformat()}),
        )
        self.audit.log(agent=self.name, event="memory_write", key=key)
```

---

## Phase 9 — Static Pipeline (Batch Scoring)

```python
# pipeline/churn_pipeline.py
from agents.signal_ingestion.agent import SignalIngestionAgent
from agents.feature_builder.agent import FeatureBuilderAgent
from agents.risk_scorer.agent import RiskScorerAgent
from agents.llm_explainer.agent import LLMExplainerAgent
from agents.personalization_strategist.agent import PersonalizationStrategistAgent
from agents.intervention.agent import InterventionAgent

class ChurnPredictionPipeline:
    """
    Deterministic batch scoring pipeline.
    PersonalizationStrategistAgent gates InterventionAgent —
    no intervention fires without a strategy decision.
    """

    def __init__(self):
        self.pre_intervention_agents = [
            SignalIngestionAgent(),
            FeatureBuilderAgent(),
            RiskScorerAgent(),
            LLMExplainerAgent(),
            PersonalizationStrategistAgent(),   # ← NEW: gates intervention
        ]
        self.intervention = InterventionAgent()

    def run(self, trigger_payload: dict) -> dict:
        payload = trigger_payload
        results = []

        for agent in self.pre_intervention_agents:
            result = agent.run(payload)
            results.append(result)

            if not result.success:
                return {"status": "failed", "failed_agent": agent.name, "results": results}

            payload = {**payload, **result.output}

        # Only route to intervention if strategist approved
        decision = payload.get("personalization_decision", {})
        if decision.get("should_personalize"):
            result = self.intervention.run(payload)
            results.append(result)
        else:
            results.append({
                "agent_name": "InterventionAgent",
                "skipped": True,
                "reason": f"priority_score {decision.get('priority_score', 0):.1f} below threshold",
            })

        return {"status": "success", "results": results, "final_payload": payload}
```

---

## Phase 10 — Claude Code Build Loop

### The workflow for each agent

Open terminal in VS Code (`Ctrl+``):

```bash
claude
```

The ⚡ icon activates. Claude can now see your open files, Problems panel, and workspace.

Example prompts for each new agent:

```
Build the PersonalizationStrategistAgent in agents/personalization_strategist/agent.py.
It inherits BaseAgent. It takes a member dict, churn_score float, and shap_features list
as payload. It scores 5 axes (customer value, business value, feasibility, confidence,
strategic alignment) each 1-10. If total < 30, should_personalize = False.
It reads MemoryAgent for prior segment learnings before scoring.
Output is a PersonalizationDecision dataclass.
```

```
Build the ExperimentationAgent in agents/experimentation/agent.py.
It inherits BaseAgent. It takes an intervention_cohort (list of member_ids),
a control_cohort, and outcome_metric (retention_rate or revenue_per_member).
It runs CUPED variance reduction, computes lift and 95% CI, checks for
confounders, and writes results to MemoryAgent with topic="intervention_outcomes".
```

```
Build the MemoryAgent in agents/memory/agent.py.
It inherits BaseAgent. It reads and writes to Redis with key schema
memory:{agent_name}:{topic}:{YYYY-MM-DD}. TTL = MEMORY_TTL_DAYS from env.
read() returns the most recent entry matching topic and optional segment.
write() stores JSON with a written_at timestamp and calls audit_log.
```

```
Build the OrchestratorAgent in agents/orchestrator/agent.py.
It inherits BaseAgent. It calls claude-sonnet-4-6 with the CEO system prompt.
It reads MemoryAgent before each task. It parses the LLM plan to decide
which agents to activate. It writes its decision back to MemoryAgent.
The system prompt is defined as a module-level constant SYSTEM_PROMPT.
```

Always review diffs before accepting. Read the diff view — Claude Code occasionally refactors adjacent files when you asked it to touch only one.

---

## Phase 11 — Git Workflow

```bash
git checkout -b feature/personalization-strategist-agent
# ... build with Claude Code ...
git add agents/personalization_strategist/ tests/unit/test_personalization_strategist.py
git commit -m "feat: add PersonalizationStrategistAgent with 5-axis scoring"
git push origin feature/personalization-strategist-agent
# Open PR → develop on GitHub
```

### GitHub Actions CI (`.github/workflows/ci.yml`)

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --tb=short
      - run: python -m mypy agents/ pipeline/ --ignore-missing-imports
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

The static pipeline (weeks 1–6) is your working foundation. Validate end-to-end before building the dynamic layer. The MemoryAgent is useless on day one and extremely valuable after 3 months of experiment results — plan for it architecturally from week 1.

---

## Director-Level Context: Why This Architecture

**The model is not the hard problem.** XGBoost on churn has been solved. The hard problems are feature freshness, auditability, and the decision layer above the model.

**Feature freshness at scale.** A nightly batch job scores members on 24-hour-old signals. A member who opened the app this morning and closed after 8 seconds will look fine in last night's batch. The streaming architecture keeps feature freshness under 90 seconds — the difference between predicting churn and reacting to it.

**The PersonalizationStrategistAgent is the missing layer.** Most churn programs treat all high-risk members identically. A 15% discount to a price-sensitive member retains them. The same offer to a convenience-driven member trains them to wait for discounts. The strategist agent decides whether to intervene at all, and if so, what form the intervention takes per segment. This is where most membership programs leave money on the table.

**Auditability is a product requirement, not a nice-to-have.** Every agent writes to the audit log before passing output downstream. You can replay any pipeline run, debug any member's score, and pass a governance review without reverse-engineering model weights.

**The MemoryAgent is the compounding asset.** After 6 months of experiments, the system knows: free-shipping extensions retain the grocery-heavy segment at 2.3x the rate of discount offers, and discount offers in the 8-14 day renewal window produce negative long-term LTV. No team has this institutionalized. Most teams re-learn it every quarter. The MemoryAgent makes every future agent session smarter than the last.

**Explainability is what makes the CRM team trust the model.** If the RiskScorerAgent says a member will churn and the CRM team cannot understand why, they will ignore it. SHAP + Claude explanation turns a probability into a story an account manager can act on.
