import pandas as pd


def recommend_response(row):
    score = row["overall_risk_score"]
    warning = row["early_warning"]

    if score >= 80:
        action = "HOLD_FOR_VERIFICATION"
        reason = (
            "Critical risk detected. Multiple risk signals "
            "require verification before proceeding."
        )

    elif score >= 60:
        action = "STEP_UP_VERIFICATION"
        reason = (
            "High risk detected. Additional verification "
            "is recommended."
        )

    elif score >= 30:
        action = "FLAG_FOR_REVIEW"
        reason = (
            "Moderate risk detected. Event should be "
            "reviewed by the risk team."
        )

    else:
        action = "ALLOW"
        reason = (
            "No significant risk signal detected."
        )

    # Escalate if risk is rapidly increasing
    if warning == 1 and score >= 50:
        if action == "ALLOW":
            action = "FLAG_FOR_REVIEW"

        reason += (
            " Risk is also showing an early-warning trend."
        )

    return pd.Series(
        {
            "recommended_action": action,
            "response_reason": reason,
            "approval_required": (
                action != "ALLOW"
            ),
            "response_status": "PENDING_APPROVAL",
        }
    )


def main():
    input_file = "data/processed/early_warning_results.csv"
    output_file = "data/processed/response_results.csv"

    df = pd.read_csv(input_file)

    response_results = df.apply(
        recommend_response,
        axis=1
    )

    df = pd.concat(
        [df, response_results],
        axis=1
    )

    df.to_csv(output_file, index=False)

    print("Response recommendation completed.")
    print(f"Saved to: {output_file}")

    print("\nRecommended actions:")
    print(
        df["recommended_action"].value_counts()
    )

    print("\nHigh-risk recommendations:")

    high_risk = df[
        df["overall_risk_score"] >= 60
    ].sort_values(
        "overall_risk_score",
        ascending=False
    )

    print(
        high_risk[
            [
                "user_id",
                "overall_risk_score",
                "risk_level",
                "recommended_action",
                "approval_required",
                "response_status",
            ]
        ].head(15).to_string(index=False)
    )


if __name__ == "__main__":
    main()
    