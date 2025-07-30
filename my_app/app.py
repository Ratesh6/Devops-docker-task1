import os
import psycopg2
import time

# Read DB credentials
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Try connecting to DB with retries
for i in range(10):
    try:
        db = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Connected to the database")
        break
    except psycopg2.OperationalError as e:
        print(f"⏳ DB not ready yet ({i+1}/10)... retrying in 3s")
        time.sleep(3)
else:
    raise Exception("❌ Could not connect to the database after several attempts")

cursor = db.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );
""")

# Insert a row
cursor.execute("INSERT INTO users (name) VALUES (%s);", ("Alice",))
db.commit()

# Read and print rows
cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()
print("All users:")
for row in rows:
    print(row)

cursor.close()
db.close()
