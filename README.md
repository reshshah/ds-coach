# DS Coach

Personal workspace for data science, ML, and AI learning — built toward Director-level DS roles at companies like Apple, Google, Netflix, Uber, DoorDash, and Anthropic.

**Philosophy:** builder first. Every concept gets implemented, not just understood.

---

## Portfolio Projects

### [AgentOps — Member Churn Prediction](https://github.com/reshshah/agentops-churn-prediction)
Production-grade multi-agent system for subscription churn prediction. Two-layer architecture: a deterministic batch scoring pipeline (XGBoost + LightGBM + SHAP + Claude explanation) and a dynamic LLM-powered layer (OrchestratorAgent, PersonalizationStrategistAgent, ExperimentationAgent, MemoryAgent). 10-week build in progress.

`multi-agent` `xgboost` `anthropic` `fastapi` `kafka` `redis` `cuped`

---

## This Repo

Documentation, project setup guides, and architecture notes for active builds. The actual project code lives in its own standalone repo (linked above).

```
projects/
└── Personalization Framework/
    ├── README.md                        ← project overview
    └── agentops_churn_project_setup.md  ← full 10-week build guide
```
