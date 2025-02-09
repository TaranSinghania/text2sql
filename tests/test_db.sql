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