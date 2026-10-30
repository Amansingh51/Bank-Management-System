import os

import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "bank_management_system"),
            port=int(os.getenv("DB_PORT", "3306"))
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection failed:", e)
        raise
