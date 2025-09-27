import mysql.connector
from faker import Faker
import random

# Setup Faker
fake = Faker()

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",   
    user="USER_NAME",        
    password="YOUR_PASS", 
    database="FRAUD_DETECTION"
)
cursor = conn.cursor()
cursor.execute("SELECT MAX(transaction_id) FROM transactions")
max_id = cursor.fetchone()[0]
if max_id is None:
    max_id = 0

def generate_transactions(n=100):
    transactions = []
    for i in range(n):
        transaction_id = max_id + i + 1
        user_id = random.randint(1, 10)  
        amount = round(random.uniform(5, 5000), 2) 
        timestamp = fake.date_time_between(start_date="-30d", end_date="now")
        location = fake.city()
        device_id = f"DEV-{random.randint(1000,9999)}"
        
        transactions.append((transaction_id, user_id, amount, timestamp, location, device_id))
    return transactions

try:
    transactions = generate_transactions(100)
    
    sql = """
    INSERT INTO transactions (transaction_id, user_id, amount, timestamp, location, device_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(sql, transactions)
    conn.commit()
    print(f"{cursor.rowcount} transactions inserted successfully!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
    conn.rollback()
    
finally:
    # Close connection
    cursor.close()
    conn.close()
