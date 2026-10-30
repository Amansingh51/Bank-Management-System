
from database import get_connection

try:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE(), VERSION()")

    result = cursor.fetchone()

    print("================================")
    print("DATABASE CONNECTION SUCCESSFUL")
    print("================================")

    print("Database:", result[0])
    print("MySQL Version:", result[1])

    cursor.execute("SHOW TABLES")

    print("\nAvailable Tables:")

    for table in cursor.fetchall():
        print("-", table[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection Error:", e)
