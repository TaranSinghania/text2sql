import sqlite3
from abc import ABC, abstractmethod
import logging

class DatabaseAbstractionLayer(ABC):
    @abstractmethod
    def execute_query(self, query: str):
        pass

class SQLiteDatabase(DatabaseAbstractionLayer):
    """
    SQLite implementation of the database abstraction layer.
    Enforces read-only mode to prevent destructive operations.
    Now returns a dictionary containing both result columns and rows.
    """
    def __init__(self, db_file: str, read_only: bool = True):
        self.db_file = db_file
        self.read_only = read_only
        logging.info("SQLiteDatabase initialized. DB_FILE: %s | READ_ONLY: %s", db_file, read_only)

    def execute_query(self, query: str):
        if self.read_only:
            destructive_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
            if any(keyword in query.upper() for keyword in destructive_keywords):
                logging.error("Attempted destructive operation in read-only mode: %s", query)
                raise Exception("Destructive operations are not allowed in read-only mode.")
        logging.info("Executing query: %s", query)
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            # Extract column names from cursor.description (if available)
            columns = [desc[0] for desc in cursor.description] if cursor.description is not None else []
            if not self.read_only:
                conn.commit()
            conn.close()
            logging.info("Query executed successfully. Rows returned: %s", len(rows))
            return {"columns": columns, "rows": rows}
        except Exception as e:
            logging.error("Error executing query: %s", e)
            raise e
