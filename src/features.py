"""Feature engineering: loads CTR data and encodes it for modelling."""

import pandas as pd
from pathlib import Path


CATEGORICAL_COLS: list[str] = ["user_gender", "ad_category", "time_of_day", "device_type"]


def load_and_encode(data_path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load CTR data from CSV and one-hot encode categorical columns.

    Uses pd.get_dummies with drop_first=True to avoid multicollinearity.
    Numeric columns (user_age) are passed through unchanged.

    Args:
        data_path: Path to ctr_data.csv.

    Returns:
        Tuple of (X, y) where X is the feature DataFrame and y is the
        binary click label Series.
    """
    df = pd.read_csv(data_path)
    y = df["clicked"]

    df = df.drop(columns=["clicked"])
    df = pd.get_dummies(df, columns=CATEGORICAL_COLS, drop_first=True)

    return df, y


def save_features(
    data_path: str | Path, output_dir: str | Path
) -> tuple[pd.DataFrame, pd.Series]:
    """Encode features and persist X and y as CSV files for downstream inspection.

    Args:
        data_path: Path to ctr_data.csv.
        output_dir: Directory where X.csv and y.csv are written.

    Returns:
        Tuple of (X, y).
    """
    X, y = load_and_encode(data_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    X.to_csv(output_dir / "X.csv", index=False)
    y.to_csv(output_dir / "y.csv", index=False)
    print(f"Saved X {X.shape} → {output_dir / 'X.csv'}")
    print(f"Saved y {y.shape} → {output_dir / 'y.csv'}")
    return X, y


if __name__ == "__main__":
    _data = Path(__file__).parents[1] / "data" / "processed" / "ctr_data.csv"
    _out = Path(__file__).parents[1] / "data" / "processed"
    save_features(_data, _out)
