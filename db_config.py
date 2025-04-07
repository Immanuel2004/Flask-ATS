import mysql.connector

def get_db_connector():
    print("Connecting to MySQL...")  # Debug message
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234567890',
        database='ats_db'
    )

