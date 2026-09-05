import pandas as pd


def investigate_event(row):
    evidence = []
    reasoning = []

    # Card-testing evidence
    if row["card_testing_score"] >= 60:
        evidence.append("Card-testing signal detected")
        reasoning.append(
            "High transaction/payment-identifier activity "
            "with an elevated failure pattern."
        )

    # ATO evidence
    if row["ato_score"] >= 60:
        evidence.append("Account-takeover signal detected")
        reasoning.append(
            "The transaction shows multiple account or "
            "behavioural risk indicators."
        )

    # Device/IP evidence
    if row["device_ip_score"] >= 60:
        evidence.append("Device/IP relationship signal detected")
        reasoning.append(
            "Multiple users, devices, or transactions are "
            "connected through shared infrastructure."
        )

    # Correlation
    if row["active_risk_signals"] >= 2:
        evidence.append("Multiple risk signals are correlated")
        reasoning.append(
            "Independent risk lenses are active at the "
            "same event, increasing overall risk."
        )

    # Overall risk interpretation
    risk_score = row["overall_risk_score"]

    if risk_score >= 80:
        recommendation = "HOLD_FOR_VERIFICATION"
    elif risk_score >= 60:
        recommendation = "STEP_UP_VERIFICATION"
    elif risk_score >= 30:
        recommendation = "FLAG_FOR_REVIEW"
    else:
        recommendation = "ALLOW"

    if risk_score >= 80:
        incident_priority = "CRITICAL"
    elif risk_score >= 60:
        incident_priority = "HIGH"
    elif risk_score >= 30:
        incident_priority = "MEDIUM"
    else:
        incident_priority = "LOW"

    return {
        "incident_priority": incident_priority,
        "evidence": " | ".join(evidence),
        "investigation_reasoning": " ".join(reasoning),
        "recommended_action": recommendation,
    }


def run_investigation(df):
    results = df.apply(
        investigate_event,
        axis=1,
        result_type="expand"
    )

    return pd.concat(
        [df, results],
        axis=1
    )


def main():
    input_file = "data/processed/risk_scores.csv"
    output_file = "data/processed/investigation_results.csv"

    df = pd.read_csv(input_file)

    df = run_investigation(df)

    df.to_csv(output_file, index=False)

    print("Investigation Agent completed.")
    print(f"Saved to: {output_file}")

    print("\nIncident priority distribution:")
    print(df["incident_priority"].value_counts())

    print("\nHigh-priority investigations:")

    high_risk = df[
        df["incident_priority"].isin(
            ["HIGH", "CRITICAL"]
        )
    ].sort_values(
        "overall_risk_score",
        ascending=False
    )

    print(
        high_risk[
            [
                "transaction_id",
                "user_id",
                "overall_risk_score",
                "risk_level",
                "incident_priority",
                "evidence",
                "recommended_action",
            ]
        ].head(10).to_string(index=False)
    )


if __name__ == "__main__":
    main()