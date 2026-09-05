import pandas as pd


INPUT_FILE = "data/processed/response_results.csv"
OUTPUT_FILE = "data/processed/incident_timeline.csv"


def build_incident_timeline(df):

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    # Focus on events showing meaningful risk
    incidents = df[
        (df["overall_risk_score"] >= 50)
        | (df["early_warning"] == 1)
    ].copy()

    incidents = incidents.sort_values(
        "timestamp"
    )

    # Create human-readable investigation stage
    def classify_stage(row):

        if row["overall_risk_score"] >= 80:
            return "CRITICAL_RISK"

        if row["early_warning"] == 1:
            return "EARLY_WARNING"

        if row["overall_risk_score"] >= 60:
            return "HIGH_RISK"

        return "SUSPICIOUS_ACTIVITY"

    incidents["investigation_stage"] = (
        incidents.apply(
            classify_stage,
            axis=1
        )
    )

    return incidents


def main():

    df = pd.read_csv(INPUT_FILE)

    timeline = build_incident_timeline(df)

    timeline.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Incident timeline created.")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nInvestigation stages:")

    print(
        timeline[
            "investigation_stage"
        ].value_counts()
    )

    print("\nTimeline:")

    print(
        timeline[
            [
                "timestamp",
                "user_id",
                "overall_risk_score",
                "investigation_stage",
                "recommended_action",
            ]
        ].head(20).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()