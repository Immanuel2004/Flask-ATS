import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connector():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'ats_db')
        )
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None

