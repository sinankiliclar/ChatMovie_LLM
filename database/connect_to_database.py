import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

def connect_to_database():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print("BAĞLANTI HATASI:", e)
        return None