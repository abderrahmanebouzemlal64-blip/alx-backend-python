#!/usr/bin/env python3
import sqlite3
import csv
import uuid
import os

DB_FILE = os.getenv("SQLITE_DB", "users.db")

# ---------- 1. Connect to SQLite ----------
def connect_db():
    try:
        connection = sqlite3.connect(DB_FILE)
        print(f"Connected to SQLite database: {DB_FILE}")
        return connection
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None


# ---------- 2. Create Table ----------
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table user ensured/created.")


# ---------- 3. Insert Data ----------
def insert_data(connection, data):
    cursor = connection.cursor()
    # Check if email already exists (to avoid duplicate inserts)
    cursor.execute("SELECT email FROM users WHERE email = ?", (data['email'],))
    result = cursor.fetchone()

    if result:
        print(f"⚠️ Skipping duplicate: {data['email']}")
    else:
        insert_query = """
        INSERT INTO users (user_id, name, email, age)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(insert_query, (
            str(uuid.uuid4()),  # Generate UUID
            data['name'],
            data['email'],
            int(data['age'])  # Ensure age is integer
        ))
        connection.commit()
        print(f"✅ Inserted: {data['email']}")


# ---------- 4. Load Data from CSV ----------
def load_csv_and_insert(connection, csv_file="user_data.csv"):
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_data(connection, row)


# ---------- MAIN ----------
if __name__ == "__main__":
    db_conn = connect_db()

    if db_conn:
        # Step 1: Create table
        create_table(db_conn)

        # Step 2: Insert CSV data
        load_csv_and_insert(db_conn, "user_data.csv")

        db_conn.close()
