import pandas as pd


INPUT_FILE = "data/processed/ai_investigation_reports.csv"

OUTPUT_FILE = "data/processed/audit_trail.csv"


def build_audit_trail(df):

    audit_columns = [
        "transaction_id",
        "timestamp",
        "user_id",
        "merchant_id",
        "overall_risk_score",
        "risk_level",
        "early_warning",
        "warning_level",
        "investigation_priority",
        "explanation",
        "evidence_source",
        "hallucination_guard",
        "recommended_action",
        "approval_required",
        "response_status",
    ]

    available_columns = [
        column
        for column in audit_columns
        if column in df.columns
    ]

    audit_df = df[available_columns].copy()

    # Add audit metadata
    audit_df["audit_event"] = "RISK_DECISION_RECORDED"

    audit_df["decision_source"] = (
        "Risk Engine + Investigation Agent + Response Agent"
    )

    audit_df["audit_status"] = "RECORDED"

    return audit_df


def main():

    df = pd.read_csv(INPUT_FILE)

    audit_df = build_audit_trail(df)

    audit_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "Audit Trail completed."
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print(
        f"\nTotal audit records: {len(audit_df)}"
    )

    print(
        "\nAudit columns:"
    )

    print(
        audit_df.columns.tolist()
    )

    print(
        "\nSample audit records:"
    )

    display_columns = [
        column
        for column in [
            "transaction_id",
            "user_id",
            "overall_risk_score",
            "investigation_priority",
            "explanation",
            "recommended_action",
            "audit_status",
        ]
        if column in audit_df.columns
    ]

    print(
        audit_df[
            display_columns
        ]
        .sort_values(
            "overall_risk_score",
            ascending=False
        )
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()