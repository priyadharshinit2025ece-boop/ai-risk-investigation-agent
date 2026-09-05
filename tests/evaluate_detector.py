import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


INPUT_FILE = "data/processed/response_results.csv"


def evaluate_detector(df):
    # Ground truth:
    # Anything other than NORMAL is considered risky
    df["actual_risk"] = (
        df["risk_label"] != "NORMAL"
    ).astype(int)

    # Prediction:
    # Overall risk >= 60 means our system flagged it
    df["predicted_risk"] = (
        df["overall_risk_score"] >= 60
    ).astype(int)

    y_true = df["actual_risk"]
    y_pred = df["predicted_risk"]

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred
    ).ravel()

    total = len(df)

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0
    )

    print("\n========== DETECTOR EVALUATION ==========")

    print(f"Total events       : {total}")
    print(f"Actual risky       : {y_true.sum()}")
    print(f"Predicted risky    : {y_pred.sum()}")

    print("\n--- Metrics ---")

    print(f"Precision          : {precision:.4f}")
    print(f"Recall             : {recall:.4f}")
    print(f"F1 Score           : {f1:.4f}")
    print(
        f"False Positive Rate: "
        f"{false_positive_rate:.4f}"
    )

    print("\n--- Confusion Matrix ---")

    print(f"True Negatives     : {tn}")
    print(f"False Positives    : {fp}")
    print(f"False Negatives    : {fn}")
    print(f"True Positives     : {tp}")

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": false_positive_rate,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }


def main():
    df = pd.read_csv(INPUT_FILE)

    evaluate_detector(df)


if __name__ == "__main__":
    main()