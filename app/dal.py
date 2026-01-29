from typing import List, Dict, Any
from db import get_db_connection

# 1 
def get_customers_by_credit_limit_range():
    """Return customers with credit limits outside the normal range."""

    sql = """
    SELECT customers.customerName, customers.creditLimit
    FROM customers
    WHERE customers.creditLimit < 10000 OR customers.creditLimit > 100000
    ORDER BY customers.creditLimit
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "creditLimit": row[1],
            }
        )

    return results

# 2 
def get_orders_with_null_comments():
    """Return orders that have null comments."""
    sql = """
    SELECT orders.orderNumber, orders.comments
    FROM orders
    WHERE orders.comments IS NULL
    ORDER BY orders.orderDate 
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "orderNumber": row[0],
                "comments": row[1],
            }
        )

    return results

# 3
def get_first_5_customers():
    """Return the first 5 customers."""
    sql = """
    SELECT customers.customerName, customers.contactLastName, customers.contactFirstName 
    FROM customers
    ORDER BY customers.contactLastName 
    LIMIT 5
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "contactLastName": row[1],
                "contactFirstName ": row[2],
            }
        )

    return results

# 4
def get_payments_total_and_average():
    """Return total and average payment amounts."""

    sql = """
    SELECT SUM(payments.amount), AVG(payments.amount),MIN(payments.amount),MAX(payments.amount)
    FROM payments
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return {
        "totalAmount": row[0],
        "averageAmount": row[1],
    }

# 5
def get_employees_with_office_phone():
    """return employees with their office phone numbers"""

    sql = """
    SELECT employees.firstName, employees.lastName, offices.phone
    FROM employees
    JOIN offices ON employees.officeCode = offices.officeCode
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "firstNamer": row[0],
                "lastName": row[1],
                "phone": row[2],
            }
        )

    return results

# 6
def get_customers_with_shipping_dates():
    """Return customers with their order shipping dates."""

    sql = """
    SELECT customers.customerName, orders.shippedDate
    FROM customers
    JOIN orders ON customers.customerNumber = orders.customerNumber
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "shippedDate": row[1],
            }
        )

    return results

# 7
def get_customer_quantity_per_order():
    """Return customer name and quantity for each order."""

    sql = """
    SELECT customers.customerName, orderdetails.quantityOrdered 
    FROM customers
    JOIN orders ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
    ORDER BY customers.customerName
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "totalQuantityOrdered": row[1],
            }
        )

    return results


# 8
def get_customers_payments_by_lastname_pattern():
    """Return customers and payments for last names matching pattern."""

    sql = """
    SELECT customers.customerName, customers.contactFirstName, SUM(payments.amount)
    FROM customers
    JOIN payments ON customers.customerNumber = payments.customerNumber
    WHERE customers.contactFirstName LIKE '%Mu%'
    OR customers.contactFirstName LIKE '%ly%'
    GROUP BY customers.customerNumber
    """

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "contactFirstName": row[1],
            }
        )