SELECT merchant_id, COUNT(*) AS transactions
FROM fact_transactions
GROUP BY merchant_id
ORDER BY transactions DESC;
