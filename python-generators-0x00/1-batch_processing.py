from itertools import islice
import importlib

batch_size = 5

def stream_users_in_batches(batch_size):
    stream_module = importlib.import_module("0-stream_users")
    stream_users = stream_module.stream_users

    for user in islice(stream_users(), batch_size):
        if user['age'] < 25:
            continue
        yield user

def batch_processing(batch_size):
    for user in islice(stream_users_in_batches(5), batch_size):
        yield user

if __name__ == "__main__":
    for user in batch_processing(5):
        print(user['age'])
