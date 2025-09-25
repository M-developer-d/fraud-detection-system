# import pymongo

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["Fraud_detection"]
# collection = db["user_logs"]

# extended_logs = [
#     {
#         "user_id": 103,
#         "login_attempts": [
#             {"timestamp": "2025-09-15T07:20:00", "ip": "192.168.2.10", "device": "Chrome-Windows"},
#             {"timestamp": "2025-09-16T09:15:00", "ip": "192.168.2.12", "device": "Chrome-Windows"},
#             {"timestamp": "2025-09-17T20:40:00", "ip": "192.168.2.15", "device": "Chrome-Windows"}
#         ],
#         "last_known_location": "Pune, India",
#         "device_history": ["Windows-PC"]
#     },
#     {
#         "user_id": 104,
#         "login_attempts": [
#             {"timestamp": "2025-09-18T08:00:00", "ip": "203.55.22.10", "device": "Safari-iPhone", "location": "London, UK"},
#             {"timestamp": "2025-09-18T12:30:00", "ip": "202.55.10.99", "device": "Chrome-Android", "location": "Mumbai, India"},
#             {"timestamp": "2025-09-18T16:10:00", "ip": "104.45.77.33", "device": "Firefox-Linux", "location": "New York, USA"}
#         ],
#         "last_known_location": "Mumbai, India",
#         "device_history": ["iPhone-14", "Android-Samsung", "Linux-Laptop"]
#     },
#     {
#         "user_id": 105,
#         "login_attempts": [
#             {"timestamp": "2025-09-17T00:05:00", "ip": "192.168.3.50", "device": "Unknown"},
#             {"timestamp": "2025-09-17T00:06:00", "ip": "192.168.3.51", "device": "Unknown"},
#             {"timestamp": "2025-09-17T00:07:00", "ip": "192.168.3.52", "device": "Unknown"},
#             {"timestamp": "2025-09-17T00:08:00", "ip": "192.168.3.53", "device": "Unknown"},
#             {"timestamp": "2025-09-17T00:09:00", "ip": "192.168.3.54", "device": "Unknown"}
#         ],
#         "last_known_location": "Bangalore, India",
#         "device_history": ["Windows-PC", "Unknown"]
#     }
# ]

# # Insert new logs
# collection.insert_many(extended_logs)

# print("✅ Extended logs inserted (users 103, 104, 105)")

# import mysql.connector
# from faker import Faker
# import random
# import numpy as np
# from datetime import datetime, timedelta

# # Setup Faker
# fake = Faker()

# # MySQL connection
# conn = mysql.connector.connect(
#     host="localhost",   # change if needed
#     user="root",        # your MySQL username
#     password="MOHAN@14_2007",  # your MySQL password
#     database="FRAUD_DETECTION"
# )
# cursor = conn.cursor()
# cursor.execute("SELECT MAX(transaction_id) FROM transactions")
# max_id = cursor.fetchone()[0]
# if max_id is None:
#     max_id = 0
# # Function to create fake transactions
# def generate_transactions(n=100):
#     transactions = []
#     for i in range(n):
#         transaction_id = max_id + i + 1
#         user_id = random.randint(1, 10)  # simulate 10 users
#         amount = round(random.uniform(5, 5000), 2)  # $5 to $5000
#         timestamp = fake.date_time_between(start_date="-30d", end_date="now")
#         location = fake.city()
#         device_id = f"DEV-{random.randint(1000,9999)}"
        
#         transactions.append((transaction_id, user_id, amount, timestamp, location, device_id))
#     return transactions

# # Generate and insert transactions
# try:
#     transactions = generate_transactions(100)
    
#     sql = """
#     INSERT INTO transactions (transaction_id, user_id, amount, timestamp, location, device_id)
#     VALUES (%s, %s, %s, %s, %s, %s)
#     """
    
#     cursor.executemany(sql, transactions)
#     conn.commit()
#     print(f"{cursor.rowcount} transactions inserted successfully!")
    
# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#     conn.rollback()
    
# finally:
#     # Close connection
#     cursor.close()
#     conn.close()



### Python Script for Anomaly Detection

import mysql.connector
import numpy as np
from datetime import datetime

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MOHAN@14_2007",
    database="FRAUD_DETECTION"
)
cursor = conn.cursor(dictionary=True)

# Fetch all transactions
cursor.execute("SELECT * FROM transactions")
transactions = cursor.fetchall()

# Convert amounts to NumPy array
amounts = np.array([t['amount'] for t in transactions])

# Compute mean & std
mean_amt = np.mean(amounts)
std_amt = np.std(amounts)

# Z-score threshold (e.g., >3 standard deviations)
threshold = 3

alerts = []

for t in transactions:
    z_score = (t['amount'] - mean_amt) / std_amt
    if abs(z_score) > threshold:
        # Flag as suspicious
        reason = f"High transaction amount (Z-score={z_score:.2f})"
        alerts.append((t['transaction_id'], t['user_id'], t['amount'], reason, datetime.now()))

# Insert alerts into fraud_alerts table
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
