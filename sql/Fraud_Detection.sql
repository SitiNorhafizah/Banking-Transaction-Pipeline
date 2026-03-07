SELECT fraud_flag, COUNT(*)
FROM fact_transactions
GROUP BY fraud_flag;
