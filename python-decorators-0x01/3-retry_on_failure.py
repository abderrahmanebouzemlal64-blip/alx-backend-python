import time
import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn=conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries, delay):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                value = func(*args, **kwargs)
                if value is not None:
                    return value
                print(f"Attempt {attempt+1} failed, retrying in {delay}s...")
                time.sleep(delay)
            print("Failed and reached max retries")
        return wrapper
    return decorator_retry

@with_db_connection
@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = 'slkdjur343sl-erkf33df345k'")
    return cursor.fetchall() or None

# ---- Usage ----
users = fetch_users_with_retry()
print(users)
