import pandas as pd


def detect_card_testing(df):
    df = df.copy()

    # Individual risk signals
    df["velocity_signal"] = (
        df["device_transaction_count"] >= 20
    ).astype(int)

    df["payment_identifier_signal"] = (
        df["unique_payment_identifiers_per_device"] >= 10
    ).astype(int)

    df["failure_signal"] = (
        df["failure_rate_by_device"] >= 0.50
    ).astype(int)

    # Combine the signals
    df["card_testing_score"] = (
        df["velocity_signal"] * 35
        + df["payment_identifier_signal"] * 35
        + df["failure_signal"] * 30
    )

    # Final detector decision
    df["card_testing_prediction"] = (
        df["card_testing_score"] >= 60
    ).astype(int)

    return df


def main():
    input_file = "data/processed/features.csv"
    output_file = "data/processed/card_testing_results.csv"

    df = pd.read_csv(input_file)

    df = detect_card_testing(df)

    df.to_csv(output_file, index=False)

    print("Card-testing detection completed.")
    print(f"Saved to: {output_file}")

    print("\nPredictions:")
    print(
        df["card_testing_prediction"]
        .value_counts()
    )

    print("\nHigh-risk transactions:")
    print(
        df[df["card_testing_prediction"] == 1][
            [
                "transaction_id",
                "device_id",
                "ip_address",
                "device_transaction_count",
                "unique_payment_identifiers_per_device",
                "failure_rate_by_device",
                "card_testing_score",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()