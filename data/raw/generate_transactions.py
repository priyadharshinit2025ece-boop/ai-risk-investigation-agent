import random
import uuid
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


NUM_TRANSACTIONS = 1000

users = [f"U{str(i).zfill(4)}" for i in range(1, 201)]
merchants = [f"M{str(i).zfill(3)}" for i in range(1, 21)]
devices = [f"D{str(i).zfill(4)}" for i in range(1, 151)]
ips = [f"IP{str(i).zfill(4)}" for i in range(1, 201)]
locations = [
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Mumbai",
    "Delhi",
    "Kolkata",
]


def generate_transaction(start_time):
    timestamp = start_time + timedelta(
        seconds=random.randint(0, 86400)
    )

    amount = round(random.uniform(50, 5000), 2)

    status = random.choices(
        ["SUCCESS", "FAILED"],
        weights=[90, 10],
    )[0]

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "user_id": random.choice(users),
        "merchant_id": random.choice(merchants),
        "amount": amount,
        "payment_status": status,
        "device_id": random.choice(devices),
        "ip_address": random.choice(ips),
        "location": random.choice(locations),
        "payment_identifier": f"CARD_{random.randint(1, 500)}",
        "account_age_days": random.randint(1, 1500),

        "credential_change" : np.random.choice([0, 1], p=[0.98, 0.02]),
        "payment_method_change" : np.random.choice([0, 1], p=[0.97, 0.03]),
    }

    return transaction


def main():
    start_time = datetime(2026, 1, 1)

    transactions = [
        generate_transaction(start_time)
        for _ in range(NUM_TRANSACTIONS)
    ]

    df = pd.DataFrame(transactions)

    output_file = "data/raw/transactions.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} transactions.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()