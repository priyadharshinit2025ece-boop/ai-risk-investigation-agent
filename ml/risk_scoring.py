import pandas as pd


def calculate_overall_risk(df):
    df = df.copy()

    # Find the strongest signal
    df["base_risk_score"] = df[
        [
            "card_testing_score",
            "ato_score",
            "device_ip_score",
        ]
    ].max(axis=1)

    # Count how many risk detectors are active
    df["active_risk_signals"] = (
        (df["card_testing_score"] >= 60).astype(int)
        + (df["ato_score"] >= 60).astype(int)
        + (df["device_ip_score"] >= 60).astype(int)
    )

    # Correlation bonus
    df["correlation_bonus"] = 0

    df.loc[
        df["active_risk_signals"] == 2,
        "correlation_bonus"
    ] = 10

    df.loc[
        df["active_risk_signals"] >= 3,
        "correlation_bonus"
    ] = 20

    # Final risk score
    df["overall_risk_score"] = (
        df["base_risk_score"]
        + df["correlation_bonus"]
    ).clip(upper=100)

    # Risk level
    def get_risk_level(score):
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        else:
            return "LOW"

    df["risk_level"] = df["overall_risk_score"].apply(
        get_risk_level
    )

    return df


def main():
    input_file = "data/processed/device_ip_results.csv"
    output_file = "data/processed/risk_scores.csv"

    df = pd.read_csv(input_file)

    df = calculate_overall_risk(df)

    df.to_csv(output_file, index=False)

    print("Overall risk scoring completed.")
    print(f"Saved to: {output_file}")

    print("\nRisk level distribution:")
    print(df["risk_level"].value_counts())

    print("\nHighest-risk events:")

    high_risk = df.sort_values(
        "overall_risk_score",
        ascending=False
    )

    print(
        high_risk[
            [
                "transaction_id",
                "user_id",
                "card_testing_score",
                "ato_score",
                "device_ip_score",
                "active_risk_signals",
                "correlation_bonus",
                "overall_risk_score",
                "risk_level",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()