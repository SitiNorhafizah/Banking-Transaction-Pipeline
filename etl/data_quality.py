import psycopg2

conn = psycopg2.connect(
    host="postgres",
    database="banking_dw",
    user="admin",
    password="admin"
)

cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM fact_transactions")
count = cur.fetchone()[0]

if count == 0:
    raise ValueError("Data quality check failed: fact_transactions is empty")

print("✅ Data quality check passed")

cur.close()
conn.close()
