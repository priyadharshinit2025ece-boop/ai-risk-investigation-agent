import pandas as pd


def add_basic_features(df):
    df = df.copy()

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort transactions chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Lists to store past-only features
    device_transaction_count = []
    unique_users_per_device = []
    unique_devices_per_ip = []
    ip_transaction_count = []
    unique_payment_identifiers_per_device = []
    failure_rate_by_device = []

    # Historical information
    device_users = {}
    ip_devices = {}
    device_payment_ids = {}
    device_total = {}
    device_failed = {}
    ip_total = {}

    # Process one transaction at a time
    for _, row in df.iterrows():

        device = row["device_id"]
        user = row["user_id"]
        ip = row["ip_address"]
        payment_id = row["payment_identifier"]

        # ---- PAST-ONLY FEATURES ----

        device_transaction_count.append(
            device_total.get(device, 0)
        )

        unique_users_per_device.append(
            len(device_users.get(device, set()))
        )

        unique_devices_per_ip.append(
            len(ip_devices.get(ip, set()))
        )

        ip_transaction_count.append(
            ip_total.get(ip, 0)
        )

        unique_payment_identifiers_per_device.append(
            len(device_payment_ids.get(device, set()))
        )

        previous_total = device_total.get(device, 0)
        previous_failed = device_failed.get(device, 0)

        if previous_total == 0:
            failure_rate_by_device.append(0.0)
        else:
            failure_rate_by_device.append(
                previous_failed / previous_total
            )

        # ---- UPDATE HISTORY AFTER CALCULATING FEATURES ----

        device_users.setdefault(device, set()).add(user)
        ip_devices.setdefault(ip, set()).add(device)
        device_payment_ids.setdefault(device, set()).add(payment_id)

        device_total[device] = (
            device_total.get(device, 0) + 1
        )

        ip_total[ip] = (
            ip_total.get(ip, 0) + 1
        )

        if row["payment_status"] == "FAILED":
            device_failed[device] = (
                device_failed.get(device, 0) + 1
            )

    # Add features to dataframe
    df["device_transaction_count"] = device_transaction_count

    df["unique_users_per_device"] = unique_users_per_device

    df["unique_devices_per_ip"] = unique_devices_per_ip

    df["ip_transaction_count"] = ip_transaction_count

    df["unique_payment_identifiers_per_device"] = (
        unique_payment_identifiers_per_device
    )

    df["failure_rate_by_device"] = failure_rate_by_device

    return df


def create_features(input_file, output_file):
    df = pd.read_csv(input_file)

    df = add_basic_features(df)

    df.to_csv(output_file, index=False)

    print("Feature engineering completed.")
    print(f"Saved to: {output_file}")
    print(f"Dataset shape: {df.shape}")


if __name__ == "__main__":
    create_features(
        "data/raw/transactions_with_risk.csv",
        "data/processed/features.csv"
    )