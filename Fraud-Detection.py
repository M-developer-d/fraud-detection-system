
import mysql.connector
import numpy as np
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="USER_NAME",
    password="YOUR_PASS",
    database="FRAUD_DETECTION"
)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT * FROM transactions")
transactions = cursor.fetchall()

amounts = np.array([t['amount'] for t in transactions])
mean_amt = np.mean(amounts)
std_amt = np.std(amounts)

threshold = 3

alerts = []

for t in transactions:
    z_score = (t['amount'] - mean_amt) / std_amt
    if abs(z_score) > threshold:
        reason = f"High transaction amount (Z-score={z_score:.2f})"
        alerts.append((t['transaction_id'], t['user_id'], t['amount'], reason, datetime.now()))

sql_insert = """
INSERT INTO fraud_alerts (transaction_id, user_id, ammount, reason, created_at)
VALUES (%s, %s, %s, %s, %s)
"""

if alerts:
    cursor.executemany(sql_insert, alerts)
    conn.commit()
    print(f"✅ {len(alerts)} suspicious transactions flagged!")
    print("Details:")
    for alert in alerts:
        print(f"Transaction ID: {alert[0]},\nUser ID: {alert[1]},\nAmount: {alert[2]},\nReason: {alert[3]} ")

else:
    print("No suspicious transactions detected.")

# Close connection
cursor.close()
conn.close()
