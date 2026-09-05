import pandas as pd


def calculate_risk_trend(df):
    df = df.copy()

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort chronologically
    df = df.sort_values(["user_id", "timestamp"])

    # Previous risk score for the same user
    df["previous_risk_score"] = (
        df.groupby("user_id")["overall_risk_score"]
        .shift(1)
    )

    # Risk increase
    df["risk_increase"] = (
        df["overall_risk_score"]
        - df["previous_risk_score"].fillna(
            df["overall_risk_score"]
        )
    )

    # Recent average risk
    df["recent_average_risk"] = (
        df.groupby("user_id")["overall_risk_score"]
        .transform(
            lambda x: x.rolling(
                window=5,
                min_periods=1
            ).mean()
        )
    )

    # Early warning conditions
    df["early_warning"] = (
        (
            (df["risk_increase"] >= 20)
            & (df["overall_risk_score"] >= 50)
        )
        |
        (
            (df["recent_average_risk"] >= 60)
            & (df["overall_risk_score"] >= 70)
        )
    ).astype(int)

    # Warning severity
    def warning_level(row):
        if row["early_warning"] == 0:
            return "NONE"

        if row["overall_risk_score"] >= 80:
            return "CRITICAL_WARNING"

        if row["overall_risk_score"] >= 60:
            return "HIGH_WARNING"

        return "MEDIUM_WARNING"

    df["warning_level"] = df.apply(
        warning_level,
        axis=1
    )

    return df


def main():
    input_file = "data/processed/investigation_results.csv"
    output_file = "data/processed/early_warning_results.csv"

    df = pd.read_csv(input_file)

    df = calculate_risk_trend(df)

    df.to_csv(output_file, index=False)

    print("Early Warning Engine completed.")
    print(f"Saved to: {output_file}")

    print("\nWarning distribution:")
    print(df["warning_level"].value_counts())

    print("\nEarly warnings:")

    warnings = df[
        df["early_warning"] == 1
    ].sort_values(
        "overall_risk_score",
        ascending=False
    )

    print(
        warnings[
            [
                "timestamp",
                "user_id",
                "overall_risk_score",
                "previous_risk_score",
                "risk_increase",
                "recent_average_risk",
                "warning_level",
            ]
        ].head(15).to_string(index=False)
    )


if __name__ == "__main__":
    main()