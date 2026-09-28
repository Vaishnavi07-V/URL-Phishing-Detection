import sqlite3
from datetime import datetime


# SQLite database file
DATABASE_NAME = "predictions.db"


# Create the database and table
def initialize_database():
    try:
        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                prediction INTEGER NOT NULL,
                result TEXT NOT NULL,
                confidence REAL,
                timestamp TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

        print("Database initialized successfully.")

    except sqlite3.Error as error:
        print("Database initialization error:", error)


# Insert a prediction into the database
def insert_prediction(url, prediction, result, confidence=None):
    try:
        connection = sqlite3.connect(DATABASE_NAME)

        cursor = connection.cursor()

        timestamp = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO predictions
            (url, prediction, result, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            url,
            prediction,
            result,
            confidence,
            timestamp
        ))

        connection.commit()

        connection.close()

        return True

    except sqlite3.Error as error:
        print("Error inserting prediction:", error)
        return False


# Retrieve prediction history
def get_prediction_history():
    try:
        connection = sqlite3.connect(DATABASE_NAME)

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                url,
                prediction,
                result,
                confidence,
                timestamp
            FROM predictions
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        connection.close()

        history = []

        for row in rows:
            history.append(dict(row))

        return history

    except sqlite3.Error as error:
        print("Error retrieving prediction history:", error)
        return []


# Initialize database when this file is run directly
if __name__ == "__main__":
    initialize_database()