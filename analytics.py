import pandas as pd


def compute_metrics(events, output_csv):
    df = pd.DataFrame(events, columns=["event", "time"])

    delays = df[df["event"] == "DELAY"]["time"]

    avg_delay = delays.mean() if len(delays) > 0 else None

    df.to_csv(output_csv, index=False)

    return avg_delay