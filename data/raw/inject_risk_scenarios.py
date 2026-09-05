import pandas as pd

INPUT_FILE = "data/raw/transactions.csv"
OUTPUT_FILE = "data/raw/transactions_with_risk.csv"


def inject_card_testing(df):
    scenario = df.iloc[0:40].copy()

    scenario["device_id"] = "D9001"
    scenario["ip_address"] = "IP9001"
    scenario["payment_status"] = "FAILED"
    scenario["amount"] = 100
    scenario["payment_identifier"] = [
        f"CARD_TEST_{i}" for i in range(len(scenario))
    ]

    scenario["risk_label"] = "CARD_TESTING"

    return scenario


def inject_ato(df):
    scenario = df.iloc[40:60].copy()

    scenario["user_id"] = "U9001"
    scenario["device_id"] = "D9002"
    scenario["ip_address"] = "IP9002"
    scenario["location"] = "Mumbai"
    scenario["account_age_days"] = 400

    scenario["risk_label"] = "ATO"

    # Simulate suspicious account/payment behaviour
    scenario.loc[scenario.index[:5], "amount"] = 50
    scenario.loc[scenario.index[5:10], "amount"] = 500
    scenario.loc[scenario.index[10:], "amount"] = 75000

    return scenario


def inject_device_ip_abuse(df):
    scenario = df.iloc[60:90].copy()

    scenario["device_id"] = "D9003"
    scenario["ip_address"] = "IP9003"

    # Multiple accounts connected to same infrastructure
    scenario["user_id"] = [
        f"U_ABUSE_{i}" for i in range(len(scenario))
    ]

    scenario["risk_label"] = "DEVICE_IP_ABUSE"

    return scenario


def main():
    df = pd.read_csv(INPUT_FILE)

    df["risk_label"] = "NORMAL"

    card_testing = inject_card_testing(df)
    ato = inject_ato(df)
    device_ip_abuse = inject_device_ip_abuse(df)

    final_df = pd.concat(
        [
            df,
            card_testing,
            ato,
            device_ip_abuse,
        ],
        ignore_index=True,
    )

    final_df.to_csv(OUTPUT_FILE, index=False)

    print("Risk scenarios injected successfully.")
    print(f"Total transactions: {len(final_df)}")
    print("\nRisk label distribution:")
    print(final_df["risk_label"].value_counts())


if __name__ == "__main__":
    main()