"""Train a Logistic Regression CTR model and persist the artifact."""

import pickle
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

from features import load_and_encode


DATA_PATH = Path(__file__).parents[1] / "data" / "processed" / "ctr_data.csv"
MODEL_PATH = Path(__file__).parents[1] / "models" / "ctr_model.pkl"


def train(
    data_path: Path = DATA_PATH,
    model_path: Path = MODEL_PATH,
    test_size: float = 0.2,
    random_state: int = 42,
) -> LogisticRegression:
    """Train a Logistic Regression model on CTR data and save it.

    Args:
        data_path: Path to the processed CSV file.
        model_path: Destination path for the pickled model.
        test_size: Fraction of data held out for evaluation.
        random_state: Seed for train/test split reproducibility.

    Returns:
        The fitted LogisticRegression model.
    """
    X, y = load_and_encode(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    model = LogisticRegression(max_iter=1000, random_state=random_state, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = (y_pred == y_test).mean()
    auc = roc_auc_score(y_test, y_prob)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"AUC-ROC  : {auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {model_path}")

    return model


if __name__ == "__main__":
    train()
