import pandas as pd
from sklearn.model_selection import train_test_split


INPUT_FILE = "data/processed/response_results.csv"

TRAIN_FILE = "data/processed/train.csv"
TEST_FILE = "data/processed/held_out_test.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    # Stratify so every risk category is represented
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["risk_label"],
    )

    train_df.to_csv(TRAIN_FILE, index=False)
    test_df.to_csv(TEST_FILE, index=False)

    print("Dataset split completed.")

    print("\nTraining set:")
    print(train_df.shape)
    print(train_df["risk_label"].value_counts())

    print("\nHeld-out test set:")
    print(test_df.shape)
    print(test_df["risk_label"].value_counts())


if __name__ == "__main__":
    main()