import sqlite3

def create_predictions_table():
    conn = sqlite3.connect("monicaheart.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        age REAL,
        cp INTEGER,
        bp REAL,
        ch REAL,
        maxhr REAL,
        std REAL,
        fluro REAL,
        th REAL,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("✅ predictions table created successfully.")

if __name__ == "__main__":
    create_predictions_table()