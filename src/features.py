"""Feature engineering: loads CTR data and encodes it for modelling."""

import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder


CATEGORICAL_COLS: list[str] = ["user_gender", "ad_category", "time_of_day", "device_type"]


def load_and_encode(data_path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load CTR data from CSV and encode categorical columns with LabelEncoder.

    Each categorical column is encoded in-place. The encoders are fitted on
    the full dataset (appropriate for offline training pipelines).

    Args:
        data_path: Path to ctr_data.csv.

    Returns:
        Tuple of (X, y) where X is the feature DataFrame and y is the
        binary click label Series.
    """
    df = pd.read_csv(data_path)

    le = LabelEncoder()
    for col in CATEGORICAL_COLS:
        df[col] = le.fit_transform(df[col])

    X = df.drop(columns=["clicked"])
    y = df["clicked"]
    return X, y


if __name__ == "__main__":
    data_path = Path(__file__).parents[1] / "data" / "processed" / "ctr_data.csv"
    X, y = load_and_encode(data_path)
    print(f"X shape: {X.shape}, click rate: {y.mean():.3f}")
