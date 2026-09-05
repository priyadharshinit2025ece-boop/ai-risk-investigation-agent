import pandas as pd


INPUT_FILE = "data/processed/response_results.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort chronologically
    df = df.sort_values("timestamp")

    # Create time buckets
    df["time_bucket"] = (
        df["timestamp"]
        .dt.floor("5min")
    )

    # Aggregate risk behaviour
    timeline = (
        df.groupby("time_bucket")
        .agg(
            average_risk=(
                "overall_risk_score",
                "mean"
            ),
            maximum_risk=(
                "overall_risk_score",
                "max"
            ),
            risky_events=(
                "overall_risk_score",
                lambda x: (x >= 60).sum()
            ),
            early_warnings=(
                "early_warning",
                "sum"
            ),
            total_events=(
                "transaction_id",
                "count"
            )
        )
        .reset_index()
    )

    timeline["risk_ratio"] = (
        timeline["risky_events"]
        / timeline["total_events"]
    )

    output_file = (
        "data/processed/risk_timeline.csv"
    )

    timeline.to_csv(
        output_file,
        index=False
    )

    print("Time-based evaluation completed.")
    print(f"Saved to: {output_file}")

    print("\nRisk timeline:")

    print(
        timeline.tail(20).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()