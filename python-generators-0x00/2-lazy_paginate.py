import seed
from itertools import islice


def lazy_paginate(page_size):
    offset= 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
        


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

if __name__ == "__main__":
    for page in islice(lazy_paginate(5), 2):
        print("=== New Page ===")
        for user in page:
            print(user)