import pandas as pd
from pathlib import Path


def main():
    df = pd.read_csv("data/transformed/events.csv")
    df["duration_minutes"] = df["duration_seconds"] / 60
    df["weekday"] = pd.to_datetime(df["date"]).dt.strftime("%A")
    Path("data/features").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/features/events.csv", index=False)
    print(f"Features: {len(df)} rows written to data/features/events.csv")


if __name__ == "__main__":
    main()
