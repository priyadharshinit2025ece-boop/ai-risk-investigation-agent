import pandas as pd


def add_basic_features(df):
    df = df.copy()

    # Make sure timestamp is treated as datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort transactions chronologically
    df = df.sort_values("timestamp")

    # Number of transactions by device
    df["device_transaction_count"] = (
        df.groupby("device_id")["transaction_id"]
        .transform("count")
    )

    # Number of users associated with each device
    df["unique_users_per_device"] = (
        df.groupby("device_id")["user_id"]
        .transform("nunique")
    )

    # Number of devices associated with each IP
    df["unique_devices_per_ip"] = (
        df.groupby("ip_address")["device_id"]
        .transform("nunique")
    )

    # Number of transactions associated with each IP
    df["ip_transaction_count"] = (
        df.groupby("ip_address")["transaction_id"]
        .transform("count")
    )

    # Number of payment identifiers associated with each device
    df["unique_payment_identifiers_per_device"] = (
        df.groupby("device_id")["payment_identifier"]
        .transform("nunique")
    )

    return df


def calculate_failure_rate(df):
    df = df.copy()

    failed = (
        df["payment_status"] == "FAILED"
    ).astype(int)

    df["failure_rate_by_device"] = (
        failed.groupby(df["device_id"])
        .transform("mean")
    )

    return df


def create_features(input_file, output_file):
    df = pd.read_csv(input_file)

    df = add_basic_features(df)
    df = calculate_failure_rate(df)

    df.to_csv(output_file, index=False)

    print("Feature engineering completed.")
    print(f"Saved to: {output_file}")
    print(f"Dataset shape: {df.shape}")


if __name__ == "__main__":
    create_features(
        "data/raw/transactions_with_risk.csv",
        "data/processed/features.csv"
    )