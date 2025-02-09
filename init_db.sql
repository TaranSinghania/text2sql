-- Drop tables if they already exist
DROP TABLE IF EXISTS airplane;
DROP TABLE IF EXISTS airport;
DROP TABLE IF EXISTS flight;
DROP TABLE IF EXISTS passenger;
DROP TABLE IF EXISTS booking;

-- Create the airplane table and insert sample data
CREATE TABLE airplane (
    id INTEGER PRIMARY KEY,
    model TEXT,
    capacity INTEGER,
    manufacturer TEXT,
    year INTEGER
);
INSERT INTO airplane (model, capacity, manufacturer, year) VALUES
('Boeing 737', 189, 'Boeing', 1997),
('Airbus A320', 180, 'Airbus', 2005);

-- Create the airport table and insert sample data
CREATE TABLE airport (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    country TEXT,
    code TEXT
);
INSERT INTO airport (name, city, country, code) VALUES
('John F. Kennedy International Airport', 'New York', 'USA', 'JFK'),
('Los Angeles International Airport', 'Los Angeles', 'USA', 'LAX');

-- Create the flight table and insert sample data
CREATE TABLE flight (
    id INTEGER PRIMARY KEY,
    airplane_id INTEGER,
    origin_airport_id INTEGER,
    destination_airport_id INTEGER,
    departure_time TEXT,
    arrival_time TEXT,
    price REAL,
    FOREIGN KEY (airplane_id) REFERENCES airplane(id),
    FOREIGN KEY (origin_airport_id) REFERENCES airport(id),
    FOREIGN KEY (destination_airport_id) REFERENCES airport(id)
);
INSERT INTO flight (airplane_id, origin_airport_id, destination_airport_id, departure_time, arrival_time, price) VALUES
(1, 1, 2, '2025-03-01 08:00:00', '2025-03-01 11:00:00', 350.00),
(2, 2, 1, '2025-03-02 09:00:00', '2025-03-02 12:30:00', 400.00);

-- Create the passenger table and insert sample data
CREATE TABLE passenger (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
);
INSERT INTO passenger (first_name, last_name, email, phone) VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890'),
('Jane', 'Smith', 'jane.smith@example.com', '0987654321');

-- Create the booking table and insert sample data
CREATE TABLE booking (
    id INTEGER PRIMARY KEY,
    passenger_id INTEGER,
    flight_id INTEGER,
    booking_date TEXT,
    seat_number TEXT,
    status TEXT,
    FOREIGN KEY (passenger_id) REFERENCES passenger(id),
    FOREIGN KEY (flight_id) REFERENCES flight(id)
);
INSERT INTO booking (passenger_id, flight_id, booking_date, seat_number, status) VALUES
(1, 1, '2025-02-25', '12A', 'confirmed'),
(2, 2, '2025-02-26', '14B', 'confirmed');

