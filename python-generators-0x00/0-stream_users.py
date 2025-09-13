#!/usr/bin/python3
from seed import connect_to_prodev

def stream_users():
    """
    Generator that streams rows one by one from the user_data table.
    Yields each row as a tuple (user_id, name, email, age).
    """
    db_conn = connect_to_prodev()
    if db_conn:
        cursor = db_conn.cursor(dictionary=True)  # not dictionary=True, keep it tuples
        cursor.execute("SELECT * FROM user_data;")

        # One loop only → generator yields each row directly
        for row in cursor:
            yield row

        cursor.close()
        db_conn.close()
