import pandas as pd


def detect_ato(df):
    df = df.copy()

    # Signal 1: suspiciously high transaction amount
    df["high_value_signal"] = (
        df["amount"] >= 50000
    ).astype(int)

    # Signal 2: account is relatively new
    df["new_account_signal"] = (
        df["account_age_days"] <= 30
    ).astype(int)

    # Signal 3: multiple users/devices are associated
    # with the same infrastructure
    df["device_relationship_signal"] = (
        df["unique_users_per_device"] >= 3
    ).astype(int)

    # Signal 4: IP is associated with multiple devices
    df["ip_relationship_signal"] = (
        df["unique_devices_per_ip"] >= 3
    ).astype(int)

    df["credential_change_signal"] = (
         df["credential_change"] == 1
    ).astype(int) * 15
    df["payment_method_change_signal"] = (
        df["payment_method_change"] == 1
    ).astype(int) * 15

    # Combine signals
    df["ato_score"] = (
        df["high_value_signal"]
        + df["new_account_signal"]
        + df["device_relationship_signal"]
        + df["ip_relationship_signal"]
        + df["credential_change_signal"]
        + df["payment_method_change_signal"]
    )

    # Detection threshold
    df["ato_prediction"] = (
        df["ato_score"] >= 60
    ).astype(int)

    return df


def main():
    input_file = "data/processed/card_testing_results.csv"
    output_file = "data/processed/ato_results.csv"

    df = pd.read_csv(input_file)

    df = detect_ato(df)

    df.to_csv(output_file, index=False)

    print("ATO detection completed.")
    print(f"Saved to: {output_file}")

    print("\nATO predictions:")
    print(df["ato_prediction"].value_counts())

    print("\nHigh-risk ATO events:")

    high_risk = df[df["ato_prediction"] == 1]

    print(
        high_risk[
            [
                "transaction_id",
                "user_id",
                "amount",
                "device_id",
                "ip_address",
                "high_value_signal",
                "new_account_signal",
                "device_relationship_signal",
                "ip_relationship_signal",
                "ato_score",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()