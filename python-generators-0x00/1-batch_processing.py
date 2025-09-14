from itertools import islice
from seed import connect_to_prodev

batch_size = 5

def stream_users_in_batches(batch_size):
    db_conn = connect_to_prodev()
    if db_conn:
        cursor = db_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

        cursor.close()
        db_conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = (user for user in batch if float(user['age']) > 25)
        for user in filtered:
            yield user

if __name__ == "__main__":
    for user in batch_processing(50):
        print(user)
