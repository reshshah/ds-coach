# Engineering Blog Research: AI, Data Science & Analytics
*Uber · Meta · DoorDash · Instacart — Top posts for webinar topics*
*Compiled: June 2026*

---

## HOW TO USE THIS FILE
Each section has: the post title + link, a 2–3 sentence summary, and a **webinar angle** — what you can extract as a teachable insight or presentation hook.

---

## UBER ENGINEERING
**Blog:** [eng.uber.com](https://eng.uber.com)

---

### 1. DeepETA: How Uber Predicts Arrival Times Using Deep Learning
[eng.uber.com](https://eng.uber.com/deepeta-how-uber-predicts-arrival-times/)

Uber replaced classical heuristic ETA models with deep learning to improve accuracy across millions of daily predictions. The model ingests real-time traffic, historical patterns, and contextual signals to generate sub-second predictions at global scale.

**Webinar angle:** Classic case study for "replacing rule-based systems with ML." Use to illustrate how the shift from heuristics to learned models requires new data infrastructure, not just a better algorithm.

---

### 2. Michelangelo: Uber's Machine Learning Platform
[eng.uber.com](https://eng.uber.com/michelangelo-machine-learning-platform/)

Uber built a unified internal ML platform — Michelangelo — to standardize how teams build, train, deploy, and monitor models. The platform handles the full lifecycle: feature engineering, distributed training, model serving, and performance monitoring.

**Webinar angle:** The canonical example for "why every data org eventually builds a platform." Key insight: **the bottleneck shifts from model quality to deployment velocity once you hit scale.** Directly applicable to Walmart, Target, or any retailer scaling DS teams.

---

### 3. Building a Backtesting Service to Measure Model Performance at Uber-scale
[eng.uber.com](https://eng.uber.com/backtesting-at-uber-scale/)

Uber built a dedicated backtesting service because standard offline metrics were insufficient for evaluating time-sensitive forecasting models. The system replays historical data under simulated conditions to measure true model degradation.

**Webinar angle:** "Evaluation is a first-class engineering problem." Most teams don't invest in proper backtesting until something breaks in production. Use this to argue for evaluation infrastructure before deployment infrastructure.

---

### 4. Food Discovery with Uber Eats: Using Graph Learning for Recommendations
[eng.uber.com](https://eng.uber.com/uber-eats-graph-learning/)

Uber Eats uses graph neural networks to capture relationships between dishes, restaurants, and users — going beyond collaborative filtering to model the structural connections in their marketplace.

**Webinar angle:** Strong example for "when collaborative filtering isn't enough." Introduce graph-based ML as the next frontier beyond traditional recommendation systems — directly relevant to e-commerce and marketplace personalization.

---

### 5. Project RADAR: Intelligent Fraud Detection with Humans in the Loop
[eng.uber.com](https://eng.uber.com/project-radar-intelligent-early-fraud-detection/)

Uber's fraud system uses ML to flag anomalies early, but deliberately keeps humans in the loop for final decisions on ambiguous cases. The architecture is designed to scale human judgment, not replace it.

**Webinar angle:** The "human-in-the-loop" design pattern. Use for webinars on AI governance, responsible AI, or change management — particularly relevant when pitching AI to risk-averse stakeholders.

---

## META ENGINEERING
**Blog:** [engineering.fb.com](https://engineering.fb.com)

---

### 1. How Meta Used AI to Map Tribal Knowledge in Large-Scale Data Pipelines *(April 2026)*
[engineering.fb.com](https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines/)

Meta built a swarm of 50+ specialized AI agents to read 4,100+ files across a complex data pipeline and produce 59 concise "context files" encoding tribal knowledge that previously lived only in engineers' heads. Result: 40% fewer AI agent tool calls per task and complex workflow guidance that used to take 2 days now takes 30 minutes.

**Webinar angle:** Powerful for the "AI-native org" topic. The insight: **AI tools fail on proprietary codebases not because they're bad models, but because they lack context.** The fix is to treat knowledge capture as an engineering problem, not a documentation problem. Direct parallel to analytics orgs where tribal knowledge lives in spreadsheets and Slack.

---

### 2. Ranking Engineer Agent (REA): Autonomous AI Accelerating Ads Ranking *(March 2026)*
[engineering.fb.com](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/)

Meta built an autonomous agent that runs the full ML experimentation lifecycle for ads ranking models — generating hypotheses, launching training jobs, debugging failures, and iterating — across multi-day workflows without continuous human supervision. Results: 2x model accuracy improvement and 5x engineering productivity (3 engineers delivered work that previously required 2 engineers per model, across 8 models).

**Webinar angle:** The clearest real-world example of **agentic AI in production ML workflows**. Key framing: the bottleneck in ML is no longer modeling skill — it's the iteration cycle. REA attacks the cycle, not the model. Use to show what "AI-native ML team" actually looks like in practice.

---

### 3. Meta's Generative Ads Model (GEM) *(November 2025)*
[engineering.fb.com](https://engineering.fb.com/2025/11/10/ml-applications/metas-generative-ads-model-gem-the-central-brain-accelerating-ads-recommendation-ai-innovation/)

Meta built a centralized generative model architecture for ads recommendation that acts as the "central brain" coordinating across ranking, retrieval, and creative optimization. GEM replaces siloed model pipelines with a unified generative system.

**Webinar angle:** The shift from **ensemble of specialized models → single generative system**. Highly relevant for anyone building ads or personalization ML. Framing: "The era of siloed models is ending. Foundation models are eating the recommendation stack."

---

### 4. Creating AI Agent Solutions for Warehouse Data Access and Security *(August 2025)*
[engineering.fb.com](https://engineering.fb.com/2025/08/13/data-infrastructure/agentic-solution-for-warehouse-data-access/)

Meta built agentic systems on top of their data warehouse to let analysts and engineers query data using natural language, while keeping row-level security and governance controls intact at the infrastructure layer.

**Webinar angle:** Direct case study for "self-serve AI analytics with guardrails." The key tension Meta solved: making data accessible without making it ungovernable. Perfect for the governance + AI access webinar topic.

---

### 5. Meta's Infrastructure Evolution and the Advent of AI *(September 2025)*
[engineering.fb.com](https://engineering.fb.com/2025/09/29/data-infrastructure/metas-infrastructure-evolution-and-the-advent-of-ai/)

Meta describes the architectural shift required to support AI at scale — moving from batch-oriented data infrastructure to real-time, AI-first pipelines that can serve models at millisecond latency across petabyte-scale data.

**Webinar angle:** Use as the "infrastructure reality check." The insight: **you cannot bolt AI onto legacy data infrastructure**. The shift to AI-native requires re-architecting data pipelines, not just adding models on top. Sobering counterpoint to hype-heavy AI talks.

---

## DOORDASH ENGINEERING
**Blog:** [careersatdoordash.com/engineering-blog](https://careersatdoordash.com/engineering-blog/)

---

### 1. Building a Unified Consumer Memory for Personalization at Scale *(June 2026)*
[careersatdoordash.com](https://careersatdoordash.com/blog/doordash-unified-consumer-memory-for-personalization-at-scale/)

DoorDash built a three-layer memory platform (long-term, in-session, explicit) that extracts semantic understanding from behavioral signals and makes it available to both traditional ML models and LLMs. Memory blocks like "dietary preferences" and "brand affinities" are versioned, encoded as dense embeddings and graph features, and served from the feature store at inference time.

**Webinar angle:** The most technically sophisticated real-world example of **LLM + ML hybrid personalization**. Key insight: behavioral data alone produces statistical patterns; semantic memory produces *understanding*. The "memory as a first-class engineering primitive" framing is highly quotable and novel.

---

### 2. Offline LLMs, Online Personalization: Generating Carousels at DoorDash
[careersatdoordash.com](https://careersatdoordash.com/blog/doordash-offline-llms-online-personalization-generating-carousels/)

DoorDash uses LLMs offline to generate personalized carousel titles and search keywords per consumer (e.g., "hydration, but make it zero sugar"), then uses those generated terms to drive real-time embedding-based retrieval. LLM cost is paid offline; personalization value is captured online.

**Webinar angle:** Elegant solution to the "LLMs are too slow for real-time personalization" objection. Introduce the **offline-generate / online-retrieve** pattern as an architecture primitive for any team building LLM-powered features.

---

### 3. How DoorDash's Brand Affinity Powers Smarter Targeting
[careersatdoordash.com](https://careersatdoordash.com/blog/doordashs-brand-affinity-powers-smarter-targeting/)

DoorDash built brand affinity signals that measure consumer-brand relationships at a semantic level — not just purchase frequency — to power more precise ad targeting and organic ranking.

**Webinar angle:** Strong case for "signals beat clicks." Brand affinity as a signal is richer than engagement history because it captures *why* someone buys, not just *what* they buy. Applicable to any ads or personalization platform.

---

### 4. Supercharging DoorDash Logistics Through Causal ML and Joint Optimization
[careersatdoordash.com](https://careersatdoordash.com/blog/supercharging-doordash-logistics-through-causal-ml-and-joint-optimization/)

DoorDash moved beyond predictive models for logistics (e.g., ETA prediction) to causal ML that estimates the effect of decisions — like batching two orders — on downstream outcomes. This enables joint optimization across the delivery network.

**Webinar angle:** The jump from **prediction → causal inference → optimization** is the maturity arc for every DS team. Use to explain why predicting outcomes isn't enough — you need to know which actions cause those outcomes to actually improve the business.

---

### 5. Lessons Learned Building DoorDash's Clusterless ML Feature Store
[careersatdoordash.com](https://careersatdoordash.com/blog/doordash-clusterless-ml-feature-store/)

DoorDash rebuilt their ML feature store to be clusterless — eliminating dedicated compute clusters for feature computation — reducing operational overhead while maintaining low-latency feature serving for production models.

**Webinar angle:** "Infrastructure simplicity is a design goal, not a consolation prize." Use to talk about **MLOps maturity**: most orgs over-engineer early infrastructure. The evolution toward simpler, more reliable systems is a sign of org maturity, not compromise.

---

## INSTACART TECH
**Blog:** [tech.instacart.com](https://tech.instacart.com) · [instacart.com/company/how-its-made](https://www.instacart.com/company/how-its-made)

---

### 1. Lessons Learned: The Journey to Real-Time Machine Learning at Instacart
[instacart.com](https://www.instacart.com/company/how-its-made/lessons-learned-the-journey-to-real-time-machine-learning-at-instacart/)

Instacart describes the architectural and organizational challenges of moving from batch ML to real-time inference — including the data pipeline changes, latency constraints, and cultural shifts required for the team to operate in a real-time world.

**Webinar angle:** Real-time ML is a **systems problem as much as a modeling problem**. The honest account of what breaks during the transition — latency, data freshness, feature drift — makes this highly credible for technical and semi-technical audiences alike.

---

### 2. How Generative AI is Revolutionizing Data Science at Instacart
[instacart.com](https://www.instacart.com/company/updates/how-generative-ai-is-revolutionizing-data-science)

Instacart describes how generative AI is changing the day-to-day workflow of their data science team — from accelerating SQL writing and EDA to generating model documentation and stakeholder-ready summaries automatically.

**Webinar angle:** Concrete answer to "what does AI-native data science actually look like day-to-day?" Instacart's framing focuses on **velocity**: the same scientist produces more analysis in less time, freeing capacity for higher-order thinking. Perfect for the mindset shift topic.

---

### 3. How Instacart Uses ML to Suggest Replacements for Out-of-Stock Products
[tech.instacart.com](https://tech.instacart.com/how-instacart-uses-machine-learning-to-suggest-replacements-for-out-of-stock-products-8f80d03bb5af)

Instacart built ML models to automatically suggest the best substitute item when a product is out of stock — combining product attributes, consumer preferences, and real-time availability to minimize order cancellations and maximize satisfaction.

**Webinar angle:** A clean, accessible ML case study where **the business problem is obvious and the ML solution is elegant**. Use as an entry-point example for mixed audiences. The insight: substitution is a ranking problem, not a search problem — framing matters.

---

### 4. AI-Driven Development at Instacart: Scaling Impact and Increasing Velocity
[instacart.com](https://www.instacart.com/company/how-its-made/ai-driven-development-at-instacart-scaling-impact-and-increasing-velocity)

Instacart describes their org-wide commitment to AI-assisted development — using AI tools across coding, testing, and documentation — with the explicit goal of increasing the output of every engineer and scientist without increasing headcount.

**Webinar angle:** Use as the **change management counterpoint**: Instacart didn't just deploy AI tools, they redesigned workflows around them. The lesson: adoption requires redesigning how work gets done, not just giving people a new tool. Strong parallel to the TripAdvisor case in your webinars.

---

### 5. Distributed Machine Learning at Instacart
[instacart.com](https://www.instacart.com/company/how-its-made/distributed-machine-learning-at-instacart/)

Instacart describes the infrastructure they built for distributed model training and serving — including how they partition data across workers, manage synchronization, and ensure consistency between offline training and online serving environments.

**Webinar angle:** Honest account of **the gap between a model that works in a notebook and a model that works in production**. Use to ground conversations about MLOps and deployment maturity. The train/serve skew problem is universal and almost always underestimated.

---

## CROSS-COMPANY THEMES FOR WEBINAR TOPICS

| Theme | Best Examples |
|---|---|
| Agentic AI in production | Meta REA, Meta Tribal Knowledge, Uber Michelangelo |
| Personalization beyond engagement signals | DoorDash Consumer Memory, DoorDash Brand Affinity, Instacart Out-of-Stock ML |
| LLM + ML hybrid architectures | DoorDash Memory Platform, DoorDash Offline LLMs / Online Retrieval |
| Real-time ML infrastructure | Instacart Real-Time ML, Uber DeepETA, DoorDash Feature Store |
| AI-native org / mindset shift | Instacart GenAI for DS, Meta REA productivity, Meta Tribal Knowledge |
| Causal ML and decision intelligence | DoorDash Causal ML, Uber Backtesting |
| Governance and guardrails | Meta Warehouse Agent, Uber RADAR (human-in-loop) |
| From analyst to architect | Meta REA, Google Cloud (prior research), Instacart AI-driven development |

---

*Sources verified June 2026. Refresh quarterly — these blogs publish frequently.*
