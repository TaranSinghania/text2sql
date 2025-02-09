import pytest
import sqlite3
from app import create_app  # Your app factory
from config import TestConfig
import time

# A complex test schema matching your test files.
TEST_SCHEMA = """
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS orders;

CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    city TEXT,
    age INTEGER
);

CREATE TABLE product (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    inventory_count INTEGER
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_date TEXT,
    quantity INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

INSERT INTO customer (first_name, last_name, email, city, age) VALUES
('Alice', 'Jones', 'alice@example.com', 'New York', 30),
('Bob', 'Smith', 'bob@example.com', 'Los Angeles', 25),
('Charlie', 'Brown', 'charlie@example.com', 'Chicago', 40);

INSERT INTO product (name, category, price, inventory_count) VALUES
('Widget A', 'Widgets', 19.99, 100),
('Widget B', 'Widgets', 29.99, 50),
('Gadget X', 'Gadgets', 49.99, 10);

INSERT INTO orders (customer_id, product_id, order_date, quantity) VALUES
(1, 2, '2025-02-15', 2),
(2, 3, '2025-02-16', 1),
(3, 1, '2025-03-01', 5);
"""

@pytest.fixture
def db_file(tmp_path):
    # Create a temporary file-based SQLite database.
    db_file = tmp_path / "test.db"
    return str(db_file)

@pytest.fixture
def app(db_file):
    # Override TestConfig.DB_FILE to use our temporary file.
    TestConfig.DB_FILE = db_file
    # Create the Flask app with the testing configuration.
    test_app = create_app()
    test_app.config.from_object(TestConfig)
    
    # Initialize the database using the TEST_SCHEMA.
    with test_app.app_context():
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        for stmt in TEST_SCHEMA.split(";"):
            stmt = stmt.strip()
            if stmt:
                cursor.execute(stmt)
        conn.commit()
        conn.close()
    
    yield test_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def delay_between_tests():
    # Yield to let the test run, then sleep for 5 second after each test.
    yield
    time.sleep(10)  # Adjust the delay (in seconds) as needed.