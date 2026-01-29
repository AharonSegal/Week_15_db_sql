dal.py
-----
```python
from db import get_db_connection


def fetch_all(sql, params=None):
    # run a select query and return all rows
    connection = get_db_connection()
    cursor = connection.cursor()

    if params is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, params)

    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def fetch_one(sql, params=None):
    # run a select query and return one row
    connection = get_db_connection()
    cursor = connection.cursor()

    if params is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, params)

    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row


def q1_customers_by_credit_limit_range():
    # customers with credit limits outside the normal range
    sql = """
    SELECT customers.customerName, customers.creditLimit
    FROM customers
    WHERE customers.creditLimit < 10000 OR customers.creditLimit > 100000
    ORDER BY customers.creditLimit
    """
    return fetch_all(sql)


def q2_orders_with_null_comments():
    # orders where comments is null
    sql = """
    SELECT orders.orderNumber, orders.comments
    FROM orders
    WHERE orders.comments IS NULL
    ORDER BY orders.orderDate
    """
    return fetch_all(sql)


def q3_first_5_customers():
    # first 5 customers ordered by contact last name
    sql = """
    SELECT customers.customerName, customers.contactLastName, customers.contactFirstName
    FROM customers
    ORDER BY customers.contactLastName
    LIMIT 5
    """
    return fetch_all(sql)


def q4_payments_total_and_average():
    # total average min and max of payments amount
    sql = """
    SELECT SUM(payments.amount), AVG(payments.amount), MIN(payments.amount), MAX(payments.amount)
    FROM payments
    """
    return fetch_one(sql)


def q5_employees_with_office_phone():
    # employees with office phone numbers
    sql = """
    SELECT employees.firstName, employees.lastName, offices.phone
    FROM employees
    JOIN offices ON employees.officeCode = offices.officeCode
    ORDER BY employees.lastName, employees.firstName
    """
    return fetch_all(sql)


def q6_customers_with_shipping_dates():
    # customers with their order shipped dates
    sql = """
    SELECT customers.customerName, orders.shippedDate
    FROM customers
    JOIN orders ON customers.customerNumber = orders.customerNumber
    ORDER BY customers.customerName, orders.shippedDate
    """
    return fetch_all(sql)


def q7_customer_quantity_per_order():
    # customer name with quantity ordered per order line
    sql = """
    SELECT customers.customerName, orderdetails.quantityOrdered
    FROM customers
    JOIN orders ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
    ORDER BY customers.customerName
    """
    return fetch_all(sql)


def q8_customers_payments_by_lastname_pattern(pattern):
    # customers with total payments where contact last name matches a pattern
    sql = """
    SELECT customers.customerName, customers.contactLastName, SUM(payments.amount)
    FROM customers
    JOIN payments ON customers.customerNumber = payments.customerNumber
    WHERE customers.contactLastName LIKE %s
    GROUP BY customers.customerNumber, customers.customerName, customers.contactLastName
    ORDER BY customers.contactLastName, customers.customerName
    """
    like_value = "%" + pattern + "%"
    return fetch_all(sql, (like_value,))
```

-----
main.py
-----
```python
from fastapi import FastAPI
from db_init import init_database
import dal

app = FastAPI()

init_database()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/q1/customers-credit-limit-outliers")
def customers_credit_limit_outliers():
    # dal returns tuples and the endpoint builds the json response
    rows = dal.q1_customers_by_credit_limit_range()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "creditLimit": row[1],
            }
        )

    return {"results": results}


@app.get("/q2/orders-null-comments")
def orders_null_comments():
    rows = dal.q2_orders_with_null_comments()

    results = []
    for row in rows:
        results.append(
            {
                "orderNumber": row[0],
                "comments": row[1],
            }
        )

    return {"results": results}


@app.get("/q3/customers-first-5")
def customers_first_5():
    rows = dal.q3_first_5_customers()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "contactLastName": row[1],
                "contactFirstName": row[2],
            }
        )

    return {"results": results}


@app.get("/q4/payments-total-average")
def payments_total_average():
    row = dal.q4_payments_total_and_average()

    return {
        "results": {
            "totalSum": row[0],
            "avgResult": row[1],
            "minPay": row[2],
            "maxPay": row[3],
        }
    }


@app.get("/q5/employees-office-phone")
def employees_office_phone():
    rows = dal.q5_employees_with_office_phone()

    results = []
    for row in rows:
        results.append(
            {
                "firstName": row[0],
                "lastName": row[1],
                "phone": row[2],
            }
        )

    return {"results": results}


@app.get("/q6/customers-shipping-dates")
def customers_shipping_dates():
    rows = dal.q6_customers_with_shipping_dates()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "shippedDate": row[1],
            }
        )

    return {"results": results}


@app.get("/q7/customer-quantity-per-order")
def customer_quantity_per_order():
    rows = dal.q7_customer_quantity_per_order()

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "quantityOrdered": row[1],
            }
        )

    return {"results": results}


@app.get("/q8/customers-payments-by-lastname-pattern")
def customers_payments_by_lastname_pattern(pattern="son"):
    # pattern is the query param and dal uses it inside a like filter
    rows = dal.q8_customers_payments_by_lastname_pattern(pattern)

    results = []
    for row in rows:
        results.append(
            {
                "customerName": row[0],
                "contactLastName": row[1],
                "totalPaymentsAmount": row[2],
            }
        )

    return {"results": results}
```