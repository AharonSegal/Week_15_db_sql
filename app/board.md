dal.py

from typing import List, Dict, Any

def get_customers_by_credit_limit_range():
    """Return customers with credit limits outside the normal range."""
    pass

def get_orders_with_null_comments():
    """Return orders that have null comments."""
    pass

def get_first_5_customers():
    """Return the first 5 customers."""
    pass

def get_payments_total_and_average():
    """Return total and average payment amounts."""
    pass

def get_employees_with_office_phone():
    """Return employees with their office phone numbers."""
    pass

def get_customers_with_shipping_dates():
    """Return customers with their order shipping dates."""
    pass

def get_customer_quantity_per_order():
    """Return customer name and quantity for each order."""
    pass

def get_customers_payments_by_lastname_pattern(pattern: str = "son"):
    """Return customers and payments for last names matching pattern."""
    pass




db_init.py

import mysql.connector
from mysql.connector import Error
import time

# Database initialization script
# Students should NOT modify this file
# This runs automatically when the server starts
# It creates the database and tables if they don't exist

def init_database():
    """
    Initializes the database by executing classicmodels.sql.
    Safe to run multiple times.
    """
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Connect to MySQL server (without specifying database)
            connection = mysql.connector.connect(
                host='mysql',
                user='root',
                password='rootpassword',
                use_pure=True
            )
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS classicmodels")
            cursor.execute("USE classicmodels")
            
            # Disable foreign key checks to allow dropping tables
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Read and execute the SQL file
            with open('/app/classicmodels.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            
            # Split and execute statements
            statements = []
            current_statement = []
            for line in sql_script.split('\n'):
                stripped = line.strip()
                if stripped and not stripped.startswith('--'):
                    current_statement.append(line)
                    if stripped.endswith(';'):
                        statements.append('\n'.join(current_statement))
                        current_statement = []
            
            # Execute each statement
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        print(f"Warning executing statement: {e}")
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print("Database initialized successfully.")
            print("Server is ready.")
            return
            
        except Error as e:
            if attempt < max_retries - 1:
                print(f"Waiting for MySQL to be ready... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print(f"Error initializing database: {e}")
                raise

if __name__ == "__main__":
    init_database()


dp.py

import mysql.connector
from mysql.connector import Error

# Simple database connection helper
# Students should NOT modify this file
# This provides a basic connection to MySQL without pooling or retries

def get_db_connection():
    """
    Returns a MySQL database connection.
    Used by dal.py functions to execute queries.
    """
    try:
        connection = mysql.connector.connect(
            host='mysql',
            user='root',
            password='rootpassword',
            database='classicmodels'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


main.py

from fastapi import FastAPI
from db_init import init_database

app = FastAPI()

init_database()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/q1/customers-credit-limit-outliers")
def customers_credit_limit_outliers():
    pass

@app.get("/q2/orders-null-comments")
def orders_null_comments():
    pass

@app.get("/q3/customers-first-5")
def customers_first_5():
    pass

@app.get("/q4/payments-total-average")
def payments_total_average():
    pass

@app.get("/q5/employees-office-phone")
def employees_office_phone():
    pass

@app.get("/q6/customers-shipping-dates")
def customers_shipping_dates():
    pass

@app.get("/q7/customer-quantity-per-order")
def customer_quantity_per_order():
    pass

@app.get("/q8/customers-payments-by-lastname-pattern")
def customers_payments_by_lastname_pattern(pattern: str = "son"):
    pass



compose
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy

dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY ["mysqlsampledatabase (1).sql", "/app/classicmodels.sql"]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




a0527@Aharon MINGW64 ~/שולחן העבודה/week_15/test/Week_15_db_sql/app (main)
$ python -u "c:\Users\a0527\שולחן העבודה\week_15\test\Week_15_db_sql\app\project_overview.py"

================= PROJECT TREE =================

dal.py
db.py
db_init.py
main.py
requirements.txt

================= PROJECT STATS =================

Total folders: 0
Total files  : 5

File types:
  .py    ->    4 files,    177 lines
  .txt   ->    1 files,      4 lines


make again look at this and add to these files only 
remember to make the sql based on the rules we said 


SHOW TABLES;

DESCRIBE customers;
DESCRIBE employees;
DESCRIBE offices;
DESCRIBE orderdetails;
DESCRIBE orders;
DESCRIBE payments;
DESCRIBE productlines;
DESCRIBE products;

SELECT COUNT(*) AS total_rows FROM customers;
SELECT COUNT(*) AS total_rows FROM employees;
SELECT COUNT(*) AS total_rows FROM offices;
SELECT COUNT(*) AS total_rows FROM orderdetails;
SELECT COUNT(*) AS total_rows FROM orders;
SELECT COUNT(*) AS total_rows FROM payments;
SELECT COUNT(*) AS total_rows FROM productlines;
SELECT COUNT(*) AS total_rows FROM products;

SELECT * FROM customers LIMIT 5;
SELECT * FROM employees LIMIT 5;
SELECT * FROM offices LIMIT 5;
SELECT * FROM orderdetails LIMIT 5;
SELECT * FROM orders LIMIT 5;
SELECT * FROM payments LIMIT 5;
SELECT * FROM productlines LIMIT 5;
SELECT * FROM products LIMIT 5;



customers
employees
offices
orderdetails
orders
payments
productlines
products


