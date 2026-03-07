import psycopg2

conn = psycopg2.connect(
    DB_HOST = os.getenv("DB_HOST",
    DB_USER = os.getenv("POSTGRES_USER"),
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
)

)
DB_PORT = os.getenv("DB_PORT")




cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM fact_transactions")
count = cur.fetchone()[0]

if count == 0:
    raise ValueError("Data quality check failed: fact_transactions is empty")

print("✅ Data quality check passed")

cur.close()
conn.close()
