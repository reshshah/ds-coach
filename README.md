# Production Data Science at Scale

Architecture patterns, build guides, and production systems for senior data science and ML engineering — written from experience building at scale.

---

## Projects

### [AgentOps — Member Churn Prediction](https://github.com/reshshah/agentops-churn-prediction)

Production-grade multi-agent system for subscription churn prediction. Two-layer architecture: a deterministic batch scoring pipeline (XGBoost + LightGBM + SHAP + Claude-powered explanation) on top of a dynamic LLM orchestration layer (OrchestratorAgent, PersonalizationStrategistAgent, ExperimentationAgent, MemoryAgent that compounds learnings across campaigns).

Feature freshness under 90 seconds via Kafka streaming. Auto-retrain on PSI drift. Every agent writes to a tamper-resistant audit log before passing output downstream. Intervention gated by a 5-axis personalization scoring model — not every high-risk member gets an offer.

`multi-agent` `xgboost` `anthropic` `fastapi` `kafka` `redis` `cuped` `shap`

---

## What's In This Repo

End-to-end build guides for production ML systems — the kind of architecture documentation that lets a team actually ship, not just design.

```
projects/
└── Personalization Framework/
    ├── README.md                        ← architecture overview
    └── agentops_churn_project_setup.md  ← 10-week production build guide
```

Each guide covers: system design decisions and tradeoffs, full folder structure, working code for every layer, CI setup, and the director-level context for *why* the architecture is built the way it is — not just what it does.

---

## Engineering Philosophy

**The model is not the hard problem.** XGBoost on churn, transformers for ranking, LLMs for summarization — these are solved. The hard problems are feature freshness, auditability, the decision layer above the model, and whether the system learns from its own interventions.

**Explainability is a product feature, not a compliance checkbox.** If the model says a member will churn and the team can't understand why, they won't act on it. SHAP + LLM explanation turns a probability into a story someone can act on.

**Every system should compound.** A churn model that runs weekly and never learns from its interventions is a static artifact. A system with a MemoryAgent that reads prior experiment outcomes before making recommendations gets measurably better after every campaign.
