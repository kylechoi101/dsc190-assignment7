import pandas as pd
from pathlib import Path


def main():
    df = pd.read_csv("data/clean/events.csv")
    df["date"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d")
    Path("data/transformed").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/transformed/events.csv", index=False)
    print(f"Transform: {len(df)} rows written to data/transformed/events.csv")


if __name__ == "__main__":
    main()
