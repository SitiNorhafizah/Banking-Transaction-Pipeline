import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

transactions = []
account_ids = [f"AC{100+i}" for i in range(20)]  # 20 accounts
merchants = ["Grab", "CarDealer", "CoffeeShop", "SuperMart", "Shop"]
channels = ["online", "pos", "atm"]
types = ["payment", "transfer", "withdrawal"]

start_time = datetime(2026, 1, 1, 8, 0)

for i in range(1000):
    # Random transaction time
    txn_time = start_time + timedelta(minutes=random.randint(0, 15000))
    
    # Random amount, 5% chance negative
    amount = round(random.uniform(1, 15000), 2)
    if random.random() < 0.05:
        amount = -amount  # inject invalid negative amounts
    
    # Random account
    account_id = random.choice(account_ids)
    
    txn = {
        "transaction_id": f"TX{i+1000}",
        "account_id": account_id,
        "timestamp": txn_time.strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "merchant": random.choice(merchants),
        "location": fake.city(),
        "transaction_type": random.choice(types),
        "channel": random.choice(channels),
        "status": "success" if random.random() > 0.01 else "failed"
    }
    transactions.append(txn)
    
    # Inject 3 rapid transactions for velocity fraud (2% of time)
    if random.random() < 0.02:
        for j in range(2):
            txn_time2 = txn_time + timedelta(seconds=random.randint(60, 180))
            txn2 = txn.copy()
            txn2["transaction_id"] = f"TX{i+1000}_{j+1}"
            txn2["timestamp"] = txn_time2.strftime("%Y-%m-%d %H:%M:%S")
            transactions.append(txn2)

df = pd.DataFrame(transactions)
df.to_csv("transactions_raw.csv", index=False)
print("✅ Sample transactions CSV generated: 1000+ rows with fraud patterns")
