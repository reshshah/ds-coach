"""End-to-end CTR prediction pipeline: data generation → features → training → comparison."""

import logging
import sys
import time
from pathlib import Path
from typing import Any, Callable

import yaml

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from data_generator import save_ctr_data
from features import save_features
from train import train as train_lr
from train_xgboost import train as train_xgb

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_config(config_path: Path) -> dict:
    """Load pipeline configuration from a YAML file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        Parsed config as a nested dict.

    Raises:
        SystemExit: If the file is missing or malformed.
    """
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        sys.exit(1)
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as exc:
        logger.error("Failed to parse config: %s", exc)
        sys.exit(1)


def run_step(step_num: int, description: str, fn: Callable, *args: Any, **kwargs: Any) -> Any:
    """Execute a pipeline step with timing, logging, and hard failure on error.

    If fn raises any exception the error is logged and the process exits
    immediately with code 1 so later steps never run on bad state.

    Args:
        step_num: Step number displayed in the header.
        description: Human-readable label for this step.
        fn: Callable to execute.
        *args: Positional arguments forwarded to fn.
        **kwargs: Keyword arguments forwarded to fn.

    Returns:
        Whatever fn returns.
    """
    logger.info("─" * 50)
    logger.info("Step %d: %s", step_num, description)
    logger.info("─" * 50)
    start = time.perf_counter()
    try:
        result = fn(*args, **kwargs)
    except Exception as exc:
        logger.error("Step %d failed: %s", step_num, exc, exc_info=True)
        sys.exit(1)
    elapsed = time.perf_counter() - start
    logger.info("Step %d complete (%.1fs)", step_num, elapsed)
    return result


def main() -> None:
    """Load config, run all pipeline steps, and log a final model comparison."""
    config = load_config(ROOT / "config.yaml")
    paths = config["paths"]
    model_cfg = config["model"]

    data_path = ROOT / paths["data"]
    features_dir = ROOT / paths["features_dir"]
    lr_model_path = ROOT / paths["lr_model"]
    xgb_model_path = ROOT / paths["xgb_model"]

    run_step(1, "Generate synthetic CTR data", save_ctr_data, data_path)

    run_step(2, "Encode features (OHE) and save to disk", save_features, data_path, features_dir)

    _, lr_auc = run_step(
        3, "Train Logistic Regression", train_lr,
        data_path=data_path,
        model_path=lr_model_path,
        test_size=model_cfg["test_size"],
    )

    _, xgb_auc = run_step(
        4, "Train XGBoost", train_xgb,
        data_path=data_path,
        model_path=xgb_model_path,
        test_size=model_cfg["test_size"],
    )

    delta = xgb_auc - lr_auc
    winner = "XGBoost" if delta > 0 else "Logistic Regression"

    logger.info("=" * 50)
    logger.info("Final Model Comparison")
    logger.info("=" * 50)
    logger.info("  %-28s  AUC-ROC    vs Baseline", "Model")
    logger.info("  %-28s  -------    -----------", "-" * 28)
    logger.info("  %-28s  %.4f     (baseline)", "Logistic Regression", lr_auc)
    sign = "+" if delta >= 0 else ""
    logger.info("  %-28s  %.4f     %s%.4f", "XGBoost", xgb_auc, sign, delta)
    logger.info("  Winner: %s", winner)
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
