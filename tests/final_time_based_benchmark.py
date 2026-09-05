import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


INPUT_FILE = "data/processed/risk_scores.csv"
OUTPUT_FILE = "data/processed/final_test_results.csv"


def main():

    # Load data
    df = pd.read_csv(INPUT_FILE)

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)

    # -------------------------------------------------
    # CHRONOLOGICAL SPLIT
    # -------------------------------------------------

    n = len(df)

    train_end = int(n * 0.70)
    validation_end = int(n * 0.85)

    train = df.iloc[:train_end].copy()
    validation = df.iloc[train_end:validation_end].copy()
    test = df.iloc[validation_end:].copy()

    print("\n========== TIME-BASED SPLIT ==========")

    print(f"Total transactions : {len(df)}")
    print(f"Train              : {len(train)}")
    print(f"Validation         : {len(validation)}")
    print(f"Final Test         : {len(test)}")

    print("\nDate ranges:")

    print(
        f"Train      : {train['timestamp'].min()} "
        f"-> {train['timestamp'].max()}"
    )

    print(
        f"Validation : {validation['timestamp'].min()} "
        f"-> {validation['timestamp'].max()}"
    )

    print(
        f"Test       : {test['timestamp'].min()} "
        f"-> {test['timestamp'].max()}"
    )

    # -------------------------------------------------
    # ACTUAL VS PREDICTED RISK
    # -------------------------------------------------

    test["actual_risk"] = (
        test["risk_label"] != "NORMAL"
    ).astype(int)

    test["predicted_risk"] = (
        test["overall_risk_score"] >= 60
    ).astype(int)

    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------

    precision = precision_score(
        test["actual_risk"],
        test["predicted_risk"],
        zero_division=0
    )

    recall = recall_score(
        test["actual_risk"],
        test["predicted_risk"],
        zero_division=0
    )

    f1 = f1_score(
        test["actual_risk"],
        test["predicted_risk"],
        zero_division=0
    )

    cm = confusion_matrix(
        test["actual_risk"],
        test["predicted_risk"]
    )

    # Handle confusion matrix safely
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()

        false_positive_rate = (
            fp / (fp + tn)
            if (fp + tn) > 0
            else 0
        )
    else:
        tn = fp = fn = tp = 0
        false_positive_rate = 0

    # -------------------------------------------------
    # PRINT RESULTS
    # -------------------------------------------------

    print("\n========== FINAL TEST RESULTS ==========")

    print(f"Precision           : {precision:.4f}")
    print(f"Recall              : {recall:.4f}")
    print(f"F1 Score            : {f1:.4f}")
    print(f"False Positive Rate : {false_positive_rate:.4f}")

    print("\nConfusion Matrix:")
    print(f"TN: {tn}")
    print(f"FP: {fp}")
    print(f"FN: {fn}")
    print(f"TP: {tp}")

    # -------------------------------------------------
    # RISK DISTRIBUTION
    # -------------------------------------------------

    print("\n========== TEST RISK DISTRIBUTION ==========")

    print(
        test["risk_label"]
        .value_counts()
    )

    # -------------------------------------------------
    # SAVE FINAL TEST DATA
    # -------------------------------------------------

    test.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nFinal test results saved to: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()