import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="ecommerce_db"
        )

        if connection.is_connected():
            return connection

    except Error as e:
        raise ConnectionError(f"[DB] Failed to connect to MySQL: {e}")

