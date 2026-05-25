#!/bin/bash

# ─────────────────────────────────────────────
# ML Project Setup Script
# Connects /Users/rshah/Documents/ml-project
# to https://github.com/reshshah/ml-project
# ─────────────────────────────────────────────

PROJECT_DIR="/Users/rshah/Documents/ml-project"
GITHUB_URL="https://github.com/reshshah/ml-project.git"

# 1. Create folder if it doesn't exist
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 2. Create ML folder structure
mkdir -p data/raw data/processed notebooks models src experiments

# 3. Create starter files
touch requirements.txt
touch src/__init__.py
touch notebooks/.gitkeep
touch experiments/.gitkeep

# 4. Write README
cat > README.md << 'EOF'
# ML Project

Ads ML experiments for big tech interviews and skill building.

## Structure
- `data/`        Raw and processed datasets
- `notebooks/`   Exploratory analysis
- `src/`         Reusable source code
- `models/`      Saved model artifacts
- `experiments/` MLflow or manual experiment logs
EOF

# 5. Write .gitignore
cat > .gitignore << 'EOF'
# Data
data/raw/
*.csv
*.parquet
*.json

# Models
models/*.pkl
models/*.pt
models/*.h5
models/*.onnx

# Python
__pycache__/
*.pyc
.env
venv/
.ipynb_checkpoints/
*.egg-info/
dist/

# System
.DS_Store
Thumbs.db
EOF

# 6. Write CLAUDE.md (Claude Code reads this every session)
cat > CLAUDE.md << 'EOF'
# Project Context for Claude Code

## Purpose
Ads ML project — building skills for ML Scientist roles at Apple, Google, Meta, DoorDash, Uber.

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
EOF

# 7. Initialize Git and connect to GitHub
git init
git remote add origin "$GITHUB_URL"

# 8. First commit and push
git add .
git commit -m "init: ML project structure with CLAUDE.md"
git branch -M main
git push -u origin main

echo ""
echo "Done. Open VS Code with: code $PROJECT_DIR"

Your daily workflow from here
# Start of day -- pull latest
git pull

# End of day -- push your work
git add .
git commit -m "describe what you did"
git push