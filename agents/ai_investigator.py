import json
import pandas as pd


INPUT_FILE = "data/processed/response_results.csv"
CLUSTER_FILE = "data/processed/risk_clusters.csv"

OUTPUT_FILE = "data/processed/ai_investigation_reports.csv"


def build_investigation_context(row, cluster=None):

    context = {
        "transaction_id": row.get("transaction_id"),
        "timestamp": str(row.get("timestamp")),
        "user_id": row.get("user_id"),
        "merchant_id": row.get("merchant_id"),
        "overall_risk_score": row.get("overall_risk_score"),
        "risk_level": row.get("risk_level"),
        "card_testing_score": row.get("card_testing_score", 0),
        "ato_score": row.get("ato_score", 0),
        "device_ip_score": row.get("device_ip_score", 0),
        "early_warning": row.get("early_warning", 0),
        "warning_level": row.get("warning_level"),
        "recommended_action": row.get(
            "recommended_action"
        ),
    }

    if cluster is not None:
        context["cluster"] = cluster

    return context


def generate_rule_based_explanation(context):

    reasons = []

    if context["card_testing_score"] >= 50:
        reasons.append(
            "card-testing behaviour detected"
        )

    if context["ato_score"] >= 50:
        reasons.append(
            "account-takeover indicators detected"
        )

    if context["device_ip_score"] >= 50:
        reasons.append(
            "suspicious device/IP relationships detected"
        )

    if context["early_warning"] == 1:
        reasons.append(
            "risk is increasing and triggered an early warning"
        )

    if not reasons:
        reasons.append(
            "no single dominant risk signal was detected"
        )

    explanation = (
        "The event received a risk score of "
        f"{context['overall_risk_score']}. "
        "The main observed signals were: "
        + "; ".join(reasons)
        + "."
    )

    return explanation


def generate_investigation_report(context):

    explanation = generate_rule_based_explanation(
        context
    )

    risk_score = context["overall_risk_score"]

    if risk_score >= 80:
        priority = "CRITICAL"
    elif risk_score >= 60:
        priority = "HIGH"
    elif risk_score >= 30:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    investigation_steps = [
        "Review the transaction and related risk signals.",
        "Check connected device and IP relationships.",
        "Review recent account activity.",
    ]

    if context["early_warning"] == 1:
        investigation_steps.append(
            "Review the recent risk trajectory because "
            "an early warning was generated."
        )

    return {
        "investigation_priority": priority,
        "explanation": explanation,
        "investigation_steps": json.dumps(
            investigation_steps
        ),
        "evidence_source": (
            "Deterministic risk signals and "
            "relationship graph"
        ),
        "hallucination_guard": (
            "Report generated only from supplied "
            "structured evidence."
        ),
    }


def main():

    df = pd.read_csv(INPUT_FILE)

    try:
        clusters = pd.read_csv(
            CLUSTER_FILE
        )
    except FileNotFoundError:
        clusters = pd.DataFrame()

    reports = []

    for _, row in df.iterrows():

        cluster_context = None

        # Cluster information will be connected
        # in the next refinement stage.
        if not clusters.empty:
            cluster_context = {
                "available": True,
                "note": (
                    "Relationship graph available "
                    "for investigation."
                )
            }

        context = build_investigation_context(
            row,
            cluster_context
        )

        report = generate_investigation_report(
            context
        )

        reports.append(report)

    report_df = pd.DataFrame(reports)

    result = pd.concat(
        [
            df.reset_index(drop=True),
            report_df.reset_index(drop=True)
        ],
        axis=1
    )

    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "AI Investigation Agent completed."
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("\nInvestigation priorities:")

    print(
        result[
            "investigation_priority"
        ].value_counts()
    )

    print("\nSample investigation reports:")

    print(
        result[
            [
                "user_id",
                "overall_risk_score",
                "investigation_priority",
                "explanation",
                "recommended_action",
            ]
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