#!/usr/bin/env python3
import mysql.connector
import os
from mysql.connector import Error
import csv
import uuid

HOST=os.getenv("MYSQL_HOST", "localhost")
USER=os.getenv("MYSQL_USER", "root")
PASSWORD = os.getenv("MYSQL_PASSWORD", "")
# ---------- 1. Connect to MySQL Server ----------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# ---------- 2. Create Database ----------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    print("Database ALX_prodev ensured/created.")


# ---------- 3. Connect to ALX_prodev Database ----------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database="ALX_prodev"
        )
        if connection.is_connected():
            print(" Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f" Error: {e}")
        return None


# ---------- 4. Create Table ----------
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL NOT NULL,
        INDEX idx_user_id (user_id)
    );
    """
    cursor.execute(create_table_query)
    print(" Table user_data ensured/created.")


# ---------- 5. Insert Data ----------
def insert_data(connection, data):
    cursor = connection.cursor()
    # Check if email already exists (to avoid duplicate inserts)
    cursor.execute("SELECT email FROM user_data WHERE email = %s", (data['email'],))
    result = cursor.fetchone()

    if result:
        print(f"⚠️ Skipping duplicate: {data['email']}")
    else:
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            str(uuid.uuid4()),  # Generate UUID
            data['name'],
            data['email'],
            data['age']
        ))
        connection.commit()
        print(f" Inserted: {data['email']}")


# ---------- 6. Load Data from CSV ----------
def load_csv_and_insert(connection, csv_file="user_data.csv"):
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_data(connection, row)


# ---------- MAIN ----------
if __name__ == "__main__":
    # Step 1: Connect to server
    server_conn = connect_db()

    if server_conn:
        # Step 2: Create database
        create_database(server_conn)
        server_conn.close()

        # Step 3: Connect to ALX_prodev
        db_conn = connect_to_prodev()

        if db_conn:
            # Step 4: Create table
            create_table(db_conn)

            # Step 5: Insert CSV data
            load_csv_and_insert(db_conn, "user_data.csv")

            db_conn.close()
