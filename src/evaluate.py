"""Reusable model evaluation utilities shared across training scripts."""

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline


def _get_importance_pairs(model: Pipeline, feature_names: list[str]) -> list[tuple[str, float]]:
    """Extract (feature, score) pairs from the pipeline's inner model.

    Handles both LogisticRegression (coef_) and tree-based models
    (feature_importances_) transparently.

    Args:
        model: Fitted sklearn Pipeline with a "model" step.
        feature_names: Ordered list of feature names.

    Returns:
        List of (feature_name, score) pairs.
    """
    clf = model.named_steps["model"]
    scores = clf.coef_[0] if hasattr(clf, "coef_") else clf.feature_importances_
    return list(zip(feature_names, scores))


def evaluate_model(
    model: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str,
    top_n: int = 10,
) -> float:
    """Print AUC-ROC, classification report, confusion matrix, and top feature importances.

    Args:
        model: Fitted sklearn Pipeline (must expose a "model" named step).
        X_test: Unscaled test features; the pipeline handles any scaling internally.
        y_test: True binary click labels.
        model_name: Display name printed in output headers.
        top_n: Number of top features to display.

    Returns:
        AUC-ROC score on the provided test set.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = (y_pred == y_test.to_numpy()).mean()
    auc = roc_auc_score(y_test, y_prob)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"AUC-ROC  : {auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    print("Confusion Matrix:")
    print(f"  {'':20} {'Predicted 0':>12} {'Predicted 1':>12}")
    print(f"  {'Actual 0 (no click)':<20} {'TN: ' + str(tn):>12} {'FP: ' + str(fp):>12}")
    print(f"  {'Actual 1 (click)':<20} {'FN: ' + str(fn):>12} {'TP: ' + str(tp):>12}")

    pairs = _get_importance_pairs(model, list(X_test.columns))
    ranked = sorted(pairs, key=lambda p: abs(p[1]), reverse=True)
    print(f"\nTop {top_n} Feature Importances:")
    print(f"  {'Feature':<35} {'Score':>10}")
    print(f"  {'-'*35} {'-'*10}")
    for name, score in ranked[:top_n]:
        print(f"  {name:<35} {score:>10.4f}")

    return auc
