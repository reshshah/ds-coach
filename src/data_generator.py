"""Generates synthetic ad click data for CTR model training."""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_ctr_data(n_rows: int = 10_000, random_seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic dataset simulating ad click behaviour.

    Args:
        n_rows: Number of rows to generate.
        random_seed: Seed for reproducibility.

    Returns:
        DataFrame with columns: user_age, user_gender, ad_category,
        time_of_day, device_type, clicked.
    """
    rng = np.random.default_rng(random_seed)

    user_age = rng.integers(18, 65, size=n_rows)
    user_gender = rng.choice(["M", "F", "Other"], size=n_rows, p=[0.48, 0.48, 0.04])
    ad_category = rng.choice(
        ["electronics", "fashion", "food", "travel", "sports"],
        size=n_rows,
    )
    time_of_day = rng.choice(
        ["morning", "afternoon", "evening", "night"],
        size=n_rows,
    )
    device_type = rng.choice(
        ["mobile", "desktop", "tablet"],
        size=n_rows,
        p=[0.60, 0.30, 0.10],
    )

    # Base CTR ~15%; simple feature interactions lift/lower probability.
    base_prob = 0.15
    age_factor = np.where(user_age < 35, 0.05, -0.02)
    device_factor = np.where(device_type == "mobile", 0.05, 0.0)
    time_factor = np.where(time_of_day == "evening", 0.04, 0.0)
    click_prob = np.clip(base_prob + age_factor + device_factor + time_factor, 0.0, 1.0)
    clicked = rng.binomial(1, click_prob).astype(int)

    return pd.DataFrame(
        {
            "user_age": user_age,
            "user_gender": user_gender,
            "ad_category": ad_category,
            "time_of_day": time_of_day,
            "device_type": device_type,
            "clicked": clicked,
        }
    )


def save_ctr_data(output_path: str | Path) -> pd.DataFrame:
    """Generate CTR data and save it as a CSV file.

    Args:
        output_path: Destination path for the CSV file.

    Returns:
        The generated DataFrame.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_ctr_data()
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df):,} rows to {output_path}")
    return df


if __name__ == "__main__":
    save_ctr_data(Path(__file__).parents[1] / "data" / "processed" / "ctr_data.csv")
