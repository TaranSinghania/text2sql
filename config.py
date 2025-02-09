import os

class Config:
    # Database settings (if you want to execute queries or store logs)
    DB_FILE = os.getenv("DB_FILE", "example.db")
    
    # Gemini API settings
    USE_GEMINI = True
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "<GEMINI API KEY>")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Flag: if False, only conversion is performed; generated SQL is not executed.
    EXECUTE_SQL = os.getenv("EXECUTE_SQL", "True") == "True"
    
    # Operational mode: enforce read-only mode.
    READ_ONLY = os.getenv("READ_ONLY", "True") == "True"
    
    # Whether to dynamically introspect the database schema at runtime.
    USE_DYNAMIC_SCHEMA = os.getenv("USE_DYNAMIC_SCHEMA", "True") == "True"
    
    # Redis settings for conversation context
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    
    # Fallback static schema information.
    STATIC_SCHEMA_INFO = {
        "airplane": {
            "columns": ["id", "model", "capacity", "manufacturer", "year"],
            "types": ["INTEGER", "TEXT", "INTEGER", "TEXT", "INTEGER"]
        },
        "flight": {
            "columns": ["id", "airplane_id", "origin_airport_id", "destination_airport_id", "departure_time", "arrival_time", "price"],
            "types": ["INTEGER", "INTEGER", "INTEGER", "INTEGER", "TEXT", "TEXT", "REAL"]
        },
        "airport": {
            "columns": ["id", "name", "city", "country", "code"],
            "types": ["INTEGER", "TEXT", "TEXT", "TEXT", "TEXT"]
        },
        "passenger": {
            "columns": ["id", "first_name", "last_name", "email", "phone"],
            "types": ["INTEGER", "TEXT", "TEXT", "TEXT", "TEXT"]
        },
        "booking": {
            "columns": ["id", "passenger_id", "flight_id", "booking_date", "seat_number", "status"],
            "types": ["INTEGER", "INTEGER", "INTEGER", "TEXT", "TEXT", "TEXT"]
        }
    }

# Separate configuration for testing.
# Separate configuration for testing.
class TestConfig(Config):
    DB_FILE = os.getenv("DB_FILE", "test.db")
    
    # Gemini API settings
    USE_GEMINI = True
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "<GEMINI API KEY>")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Flag: if False, only conversion is performed; generated SQL is not executed.
    EXECUTE_SQL = os.getenv("EXECUTE_SQL", "True") == "True"
    
    # Operational mode: enforce read-only mode.
    READ_ONLY = os.getenv("READ_ONLY", "True") == "True"
    
    # Whether to dynamically introspect the database schema at runtime.
    USE_DYNAMIC_SCHEMA = os.getenv("USE_DYNAMIC_SCHEMA", "True") == "True"
    
    # Redis settings for conversation context
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    # Test schema based on the test files.
    STATIC_SCHEMA_INFO = {
        "customer": {
            "columns": ["id", "first_name", "last_name", "email", "city", "age"],
            "types": ["INTEGER", "TEXT", "TEXT", "TEXT", "TEXT", "INTEGER"]
        },
        "product": {
            "columns": ["id", "name", "category", "price", "inventory_count"],
            "types": ["INTEGER", "TEXT", "TEXT", "REAL", "INTEGER"]
        },
        "orders": {
            "columns": ["id", "customer_id", "product_id", "order_date", "quantity"],
            "types": ["INTEGER", "INTEGER", "INTEGER", "TEXT", "INTEGER"]
        },
        "conversion_log": {
            "columns": ["id", "user_id", "query", "generated_sql", "timestamp"],
            "types": ["INTEGER", "TEXT", "TEXT", "TEXT", "DATETIME"]
        }
    }
