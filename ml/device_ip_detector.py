import pandas as pd


def detect_device_ip_relationships(df):
    df = df.copy()

    # Signal 1:
    # Many different users connected to the same device
    df["shared_device_signal"] = (
        df["unique_users_per_device"] >= 3
    ).astype(int)

    # Signal 2:
    # Many devices connected to the same IP
    df["shared_ip_signal"] = (
        df["unique_devices_per_ip"] >= 3
    ).astype(int)

    # Signal 3:
    # High number of transactions through the IP
    df["ip_velocity_signal"] = (
        df["ip_transaction_count"] >= 20
    ).astype(int)

    # Combine relationship signals
    df["device_ip_score"] = (
        df["shared_device_signal"] * 40
        + df["shared_ip_signal"] * 30
        + df["ip_velocity_signal"] * 30
    )

    # Detection threshold
    df["device_ip_prediction"] = (
        df["device_ip_score"] >= 60
    ).astype(int)

    return df


def main():
    input_file = "data/processed/ato_results.csv"
    output_file = "data/processed/device_ip_results.csv"

    df = pd.read_csv(input_file)

    df = detect_device_ip_relationships(df)

    df.to_csv(output_file, index=False)

    print("Device/IP relationship detection completed.")
    print(f"Saved to: {output_file}")

    print("\nPredictions:")
    print(df["device_ip_prediction"].value_counts())

    print("\nHigh-risk relationships:")

    high_risk = df[df["device_ip_prediction"] == 1]

    print(
        high_risk[
            [
                "transaction_id",
                "user_id",
                "device_id",
                "ip_address",
                "unique_users_per_device",
                "unique_devices_per_ip",
                "ip_transaction_count",
                "device_ip_score",
            ]
        ].head(10)
    )


if __name__ == "__main__":
    main()