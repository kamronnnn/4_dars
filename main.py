import psycopg2 as sql

db = sql.connect(
    database="auto",
    host="localhost",
    user="postgres",
    password="123456",
    port="5432"
)
cur = db.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS brands (
        brand_id SERIAL PRIMARY KEY,
        brand_name VARCHAR(50) NOT NULL,
        brand_color VARCHAR(20)
    );

    CREATE TABLE IF NOT EXISTS models (
        model_id SERIAL PRIMARY KEY,
        model_name VARCHAR(50) NOT NULL,
        brand_id INTEGER REFERENCES brands(brand_id),
        price DECIMAL(10, 2)
    );

    CREATE TABLE IF NOT EXISTS employees (
        employee_id SERIAL PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        email VARCHAR(50) UNIQUE
    );

    CREATE TABLE IF NOT EXISTS customers (
        customer_id SERIAL PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        email VARCHAR(50) UNIQUE
    );

    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INTEGER REFERENCES customers(customer_id),
        employee_id INTEGER REFERENCES employees(employee_id),
        model_id INTEGER REFERENCES models(model_id),
        order_date DATE
    );
""")

cur.execute("""
    INSERT INTO brands (brand_name, brand_color) VALUES
    ('Toyota', 'Qizil'),
    ('Honda', 'Moviy'),
    ('BMW', 'Qora');

    INSERT INTO models (model_name, brand_id, price) VALUES
    ('Corolla', 1, 20000),
    ('Accord', 2, 25000),
    ('X5', 3, 60000);

    INSERT INTO employees (first_name, last_name, email) VALUES
    ('Toxir', 'Toxirov', 'toxir@gmail.com'),
    ('Jalil', 'Jalilov', 'jalil@gmail.com');

    INSERT INTO customers (first_name, last_name, email) VALUES
    ('Sobir', 'Sobirov', 'sobir@gmail.com'),
    ('Bobir', 'Bobirov', 'bobir@gmail.com');

    INSERT INTO orders (customer_id, employee_id, model_id, order_date) VALUES
    (1, 1, 1, '2024-02-15'),
    (2, 2, 2, '2024-02-15');
""")

cur.execute("""
    SELECT models.model_name, brands.brand_name, brands.brand_color
    FROM models
    JOIN brands ON models.brand_id = brands.brand_id;

    SELECT email FROM employees
    UNION
    SELECT email FROM customers;

    SELECT country, COUNT(employee_id) AS employee_count
    FROM employees
    GROUP BY country
    ORDER BY employee_count DESC;

    SELECT brands.brand_name, COUNT(models.model_id) AS model_count
    FROM brands
    JOIN models ON brands.brand_id = models.brand_id
    GROUP BY brands.brand_name;

    SELECT brands.brand_name
    FROM brands
    JOIN models ON brands.brand_id = models.brand_id
    GROUP BY brands.brand_name
    HAVING COUNT(models.model_id) > 5;

    SELECT orders.order_id, customers.first_name AS customer_first_name, employees.first_name AS employee_first_name, models.model_name
    FROM orders
    JOIN customers ON orders.customer_id = customers.customer_id
    JOIN employees ON orders.employee_id = employees.employee_id
    JOIN models ON orders.model_id = models.model_id;

    SELECT SUM(price) AS total_price
    FROM models;
""")

rows = cur.fetchall()
for row in rows:
    print(row)

db.close()
db.commit()
