# Project Context for Claude Code

## Purpose
Ads ML project — building skills for ML Scientist roles

## Stack
- Python 3.11+
- pandas, numpy, scikit-learn, PyTorch
- MLflow for experiment tracking
- pytest for testing

## Folder Structure
- data/raw        → never modify, never commit
- data/processed  → cleaned, feature-engineered data
- notebooks/      → EDA and prototyping only
- src/            → production-grade reusable code
- models/         → serialized model artifacts
- experiments/    → experiment configs and results

## Coding Conventions
- Type hints on all functions
- Docstrings on all public functions
- No hardcoded paths — use config files
- Each experiment gets its own subfolder in experiments/
