import sqlite3
import pandas as pd
conn = sqlite3.Connection('data.sqlite')


# Check the tables in the database
print("\n", "Tables in the database:", "\n\n", pd.read_sql("""SELECT name FROM sqlite_master WHERE type='table';""", conn), "\n")

# Check the columns in the orderdetails table
print("\n", "Columns in orderdetails table:", "\n\n", pd.read_sql("""PRAGMA table_info('orderdetails');""", conn), "\n")

# Check the columns in the payments table
print("\n", "Columns in payments table:", "\n\n", pd.read_sql("""PRAGMA table_info('payments');""", conn), "\n")

# Check the columns in the offices table
print("\n", "Columns in offices table:", "\n\n", pd.read_sql("""PRAGMA table_info('offices');""", conn), "\n")

# Check the columns in the customers table
print("\n", "Columns in customers table:", "\n\n", pd.read_sql("""PRAGMA table_info('customers');""", conn), "\n")

# Check the columns in the orders table
print("\n", "Columns in orders table:", "\n\n", pd.read_sql("""PRAGMA table_info('orders');""", conn), "\n")

# Check the columns in the productlines table
print("\n", "Columns in productlines table:", "\n\n", pd.read_sql("""PRAGMA table_info('productlines');""", conn), "\n")

# Check the columns in the products table
print("\n", "Columns in products table:", "\n\n", pd.read_sql("""PRAGMA table_info('products');""", conn), "\n")

# Check the columns in the employees table
print("\n", "Columns in employees table:", "\n\n", pd.read_sql("""PRAGMA table_info('employees');""", conn), "\n")


# JOIN employees and offices tables to get the last name, first name, and office code
# of employees working in the USA
q = """
SELECT lastName, firstName, officeCode
FROM employees
JOIN offices
    USING(officeCode)
WHERE country = "USA"
;"""
print(pd.read_sql(q, conn))
print("\n")

# Same as above, but using a subquery instead of a JOIN
q = """
SELECT lastName, firstName, officeCode
FROM employees
WHERE officeCode IN (SELECT officeCode
                     FROM offices 
                     WHERE country = "USA")
;
"""
print(pd.read_sql(q, conn))
print("\n")



# Get the last name, first name, and office code of employees working in offices
q = """
SELECT lastName, firstName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode 
    FROM offices 
    JOIN employees
        USING(officeCode)
    GROUP BY 1
    HAVING COUNT(employeeNumber) >= 5
)
;
"""
print(pd.read_sql(q, conn))
print("\n")



# Getting the average payment amount for each customer, and then the average of those averages
q = """
SELECT AVG(customerAvgPayment) AS averagePayment
FROM (
    SELECT AVG(amount) AS customerAvgPayment
    FROM payments
    JOIN customers
        USING(customerNumber)
    GROUP BY customerNumber
)
;"""
print(pd.read_sql(q, conn))
print("\n")



# Get the last name, first name, and employee number of employees
# who are sales representatives for customers in the USA
q = """
SELECT lastName, firstName, employeeNumber
FROM employees
WHERE employeeNumber IN (SELECT salesRepEmployeeNumber
                     FROM customers 
                     WHERE country = "USA")
;
"""
print(pd.read_sql(q, conn))
print("\n")

conn.close()