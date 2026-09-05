import pandas as pd
from sklearn.metrics import confusion_matrix


INPUT_FILE = "data/processed/held_out_test.csv"

FALSE_POSITIVE_COST = 10
FALSE_NEGATIVE_COST = 500


def main():
    df = pd.read_csv(INPUT_FILE)

    actual = (
        df["risk_label"] != "NORMAL"
    ).astype(int)

    predicted = (
        df["overall_risk_score"] >= 60
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        actual,
        predicted
    ).ravel()

    fp_cost = fp * FALSE_POSITIVE_COST
    fn_cost = fn * FALSE_NEGATIVE_COST

    total_cost = fp_cost + fn_cost

    print("========== RISK COST ANALYSIS ==========")

    print(f"False positives : {fp}")
    print(f"False negatives : {fn}")

    print("\nPrototype cost assumptions:")
    print(
        f"False positive cost: "
        f"₹{FALSE_POSITIVE_COST}"
    )
    print(
        f"False negative cost: "
        f"₹{FALSE_NEGATIVE_COST}"
    )

    print("\nEstimated impact:")

    print(f"FP cost          : ₹{fp_cost}")
    print(f"FN cost          : ₹{fn_cost}")
    print(f"Total estimated  : ₹{total_cost}")


if __name__ == "__main__":
    main()
    