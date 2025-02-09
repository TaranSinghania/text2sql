# app/models/schema_manager.py

from difflib import get_close_matches
import sqlite3
import logging

class SchemaManager:
    """
    Provides schema information and supports fuzzy matching.
    If dynamic introspection is enabled, fetches the schema from the database.
    """
    def __init__(self, schema_info: dict = None, db_file: str = None, use_dynamic_schema: bool = False):
        if use_dynamic_schema:
            if not db_file:
                raise ValueError("db_file is required for dynamic schema introspection")
            logging.info("Using dynamic schema introspection from DB file: %s", db_file)
            self.schema_info = self.fetch_schema(db_file)
        else:
            self.schema_info = schema_info or {}
            logging.info("Using static schema information.")
        logging.debug("SchemaManager initialized with schema: %s", self.schema_info)

    def fetch_schema(self, db_file: str) -> dict:
        schema_info = {}
        logging.info("Fetching schema from database: %s", db_file)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        logging.info("Found tables: %s", tables)
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            info = cursor.fetchall()  # Each row: (cid, name, type, notnull, dflt_value, pk)
            columns = [row[1] for row in info]
            types = [row[2] for row in info]
            schema_info[table] = {"columns": columns, "types": types}
            logging.info("Table %s: columns %s", table, columns)
        conn.close()
        return schema_info

    def get_schema(self) -> dict:
        return self.schema_info

    def correct_term(self, term: str, schema_terms: list) -> str:
        matches = get_close_matches(term.lower(), [s.lower() for s in schema_terms], n=1, cutoff=0.8)
        if matches:
            for s in schema_terms:
                if s.lower() == matches[0]:
                    logging.info("Corrected term '%s' to '%s'", term, s)
                    return s
        logging.info("No correction found for term '%s'", term)
        return term
