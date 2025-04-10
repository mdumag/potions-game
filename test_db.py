# test_db.py

from src.database import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            row = result.fetchone()
            if row is not None:
                print("Connection successful, test result:", row)
            else:
                print("Connection established but no result returned")
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()
