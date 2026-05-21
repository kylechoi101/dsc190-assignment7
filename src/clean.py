import pandas as pd
from pathlib import Path
from datetime import datetime

VALID_EVENT_TYPES = {"click", "login", "scroll", "view", "buy", "purchase"}


def parse_timestamp(ts: str) -> str | None:
    ts = ts.strip()
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(ts, fmt).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return None


def main():
    df = pd.read_csv("data/raw/events.csv", dtype=str)

    # Drop rows with any missing/empty fields
    df = df.dropna()
    df = df[df.apply(lambda r: all(v.strip() != "" for v in r), axis=1)]

    # Drop invalid event types
    df = df[df["event_type"].isin(VALID_EVENT_TYPES)]

    # Drop non-positive duration_seconds
    df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="coerce")
    df = df.dropna(subset=["duration_seconds"])
    df = df[df["duration_seconds"] > 0]

    # Normalize timestamps
    df["timestamp"] = df["timestamp"].apply(parse_timestamp)
    df = df.dropna(subset=["timestamp"])

    Path("data/clean").mkdir(parents=True, exist_ok=True)
    df.to_csv("data/clean/events.csv", index=False)
    print(f"Clean: {len(df)} rows written to data/clean/events.csv")


if __name__ == "__main__":
    main()
