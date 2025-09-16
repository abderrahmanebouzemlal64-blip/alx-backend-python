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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)

            if result is not None:
                conn.commit()
                print("✅ results committed", result)
                return result
            else:
                conn.rollback()
                print(result)
                raise Exception("Transaction failed")
        except Exception as e:
            print(e)
    return wrapper
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE user_id = ?", (new_email, user_id))
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()


# ---- Example usage ----
update_user_email(user_id='1', new_email='Crawford_Cartwright@hotmail.com')
