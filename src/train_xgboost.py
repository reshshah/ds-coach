"""Train an XGBoost CTR model and persist the artifact."""

import pickle
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from evaluate import evaluate_model
from features import load_and_encode


DATA_PATH = Path(__file__).parents[1] / "data" / "processed" / "ctr_data.csv"
MODEL_PATH = Path(__file__).parents[1] / "models" / "ctr_xgboost.pkl"


def train(
    data_path: Path = DATA_PATH,
    model_path: Path = MODEL_PATH,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[Pipeline, float]:
    """Train an XGBoost pipeline on CTR data and save it.

    StandardScaler is included for consistency with the LR baseline, though
    tree-based models are invariant to monotonic feature transformations.

    Args:
        data_path: Path to the processed CSV file.
        model_path: Destination path for the pickled pipeline.
        test_size: Fraction of data held out for evaluation.
        random_state: Seed for train/test split reproducibility.

    Returns:
        Tuple of (fitted Pipeline, AUC-ROC score on test set).
    """
    X, y = load_and_encode(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            scale_pos_weight=4,
            random_state=random_state,
            eval_metric="logloss",
            verbosity=0,
        )),
    ])
    pipeline.fit(X_train, y_train)

    auc = evaluate_model(pipeline, X_test, y_test, "XGBoost")

    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"\nModel saved to {model_path}")

    return pipeline, auc


if __name__ == "__main__":
    train()
