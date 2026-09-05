from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


REQUIRED_FILES = [
    "features.csv",
    "risk_scores.csv",
    "risk_timeline.csv",
    "incident_timeline.csv",
    "response_results.csv",
    "risk_graph_nodes.csv",
    "risk_graph_edges.csv",
    "risk_clusters.csv",
    "ai_investigation_reports.csv",
    "audit_trail.csv",
    "final_test_results.csv",
]


def main():

    print("\n======================================")
    print("END-TO-END SYSTEM CHECK")
    print("======================================")

    failed = False

    for filename in REQUIRED_FILES:

        path = DATA_DIR / filename

        if not path.exists():

            print(f"❌ MISSING: {filename}")
            failed = True
            continue

        try:

            df = pd.read_csv(path)

            print(
                f"✅ {filename:<35} "
                f"{len(df):>6} rows"
            )

        except Exception as error:

            print(
                f"❌ INVALID: {filename}"
            )

            print(f"   Error: {error}")

            failed = True

    print("\n--------------------------------------")

    if failed:

        print("❌ END-TO-END CHECK FAILED")

        raise SystemExit(1)

    print("✅ ALL REQUIRED OUTPUTS AVAILABLE")

    print("--------------------------------------")

    # -------------------------------------------------
    # Basic consistency checks
    # -------------------------------------------------

    response = pd.read_csv(
        DATA_DIR / "response_results.csv"
    )

    investigation = pd.read_csv(
        DATA_DIR / "ai_investigation_reports.csv"
    )

    audit = pd.read_csv(
        DATA_DIR / "audit_trail.csv"
    )

    checks = []

    checks.append(
        len(response) > 0
    )

    checks.append(
        len(investigation) > 0
    )

    checks.append(
        len(audit) > 0
    )

    if "transaction_id" in response.columns:
        checks.append(
            response["transaction_id"]
            .notna()
            .all()
        )

    if "overall_risk_score" in response.columns:
        checks.append(
            response["overall_risk_score"]
            .notna()
            .all()
        )

    if all(checks):

        print("✅ DATA CONSISTENCY CHECK PASSED")

    else:

        print("❌ DATA CONSISTENCY CHECK FAILED")

        raise SystemExit(1)

    print("\n🎯 END-TO-END DATA PIPELINE: PASS")


if __name__ == "__main__":
    main()