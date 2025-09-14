from seed import connect_to_prodev

def stream_user_ages():
    db_conn = connect_to_prodev()
    if db_conn:
        cursor = db_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        for user in cursor:
            yield user['age']

        cursor.close()
        db_conn.close()

def average_users():
    sumation = 0
    count = 0
    for age in stream_user_ages():
        sumation += age
        count += 1
    return sumation / count

average = average_users()
print(average) 