# Bank Management System — Project Report

## 1. Abstract

The Bank Management System is a Flask-based web application for common account-management tasks. It provides pages to view bank summaries, register customers, list accounts, record deposits and withdrawals, check balances, and review transaction history. MySQL is used as the persistence layer, with several business operations delegated to stored procedures and a database function.

## 2. Problem statement

Basic banking records need to be organized so that customer accounts and their transactions can be viewed and updated through a consistent interface. This project demonstrates a small web application that connects a browser-based interface to a relational database for those operations.

## 3. Objectives

- Provide a dashboard summarizing customers, accounts, balances, and recent transactions.
- Support creating customers with an opening deposit.
- Display customer and account records.
- Support account deposits, withdrawals, balance lookups, and transaction-history searches.
- Demonstrate integration between Flask, HTML templates, and MySQL.

## 4. Scope and features

The current application contains the following routes:

| Route | Functionality |
| --- | --- |
| `/` | Displays customer and account counts, the total account balance, and recent transactions. |
| `/customers` | Accepts customer details and an opening deposit, and displays customer/account rows. |
| `/accounts` | Displays account IDs, customer names, phone numbers, and balances. |
| `/deposit` | Validates an account ID and positive amount, performs a deposit, and displays balances. |
| `/withdraw` | Validates a withdrawal against the account's current balance and performs it when funds are sufficient. |
| `/balance` | Looks up an account balance. |
| `/history` | Displays transaction history for a selected account. |

## 5. Technology stack

- **Language:** Python
- **Web framework:** Flask
- **Database:** MySQL
- **Database driver:** `mysql-connector-python`
- **Presentation:** HTML templates rendered with Jinja

## 6. System design

The browser sends requests to Flask route handlers in `app.py`. Those handlers render pages from the `templates/` directory and use helper functions in `app.py` to query MySQL. The connection is created by `get_connection()` in `database.py`.

The code calls MySQL routines for customer/account creation, deposits, withdrawals, and transaction-history retrieval. It queries customer and account totals and recent transactions directly. Database transactions for routine calls are committed on success and rolled back when an error occurs.

The expected database entities and routines are listed in the README. Their schema and definitions are not currently supplied: `database/bank_management.sql` is empty. A compatible MySQL database must therefore be set up before the application can perform its data-backed operations.

## 7. Data flow

1. A user opens a page or submits an HTML form.
2. Flask validates basic input such as required customer name, positive account ID, and positive transaction amount.
3. The route executes a parameterized SQL query or calls the corresponding MySQL routine.
4. Results or status messages are passed to a Jinja template.
5. The template renders the response in the browser.

## 8. Running the application

1. Install Python and MySQL Server.
2. Create and activate a Python virtual environment.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Create the `bank_management_system` database and all required tables, procedures, and function. Configure the `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, and `DB_PORT` environment variables for the local MySQL connection.
5. Run `python app.py` and open `http://127.0.0.1:5000`.
6. Optionally run `python test_db.py` to check the database connection and list tables.

See [README.md](./README.md) for the detailed database requirements and commands.

## 9. Testing

The repository includes `test_db.py`, a manual database-connection check that queries the active database and MySQL version and lists tables. No automated application test suite is currently included. The app requires a correctly configured MySQL server and the expected database routines for end-to-end testing.

## 10. Limitations and future improvements

- The SQL schema, stored-procedure definitions, and balance function need to be added to the currently empty SQL file.
- Database credentials must be kept in local environment configuration and out of source control.
- Authentication, authorization, audit controls, and production-grade security are not implemented.
- Automated tests should cover validation, successful operations, insufficient funds, and database failures.
- Currency handling and database constraints should be standardized and documented.
- The development server is started with Flask's debug mode; production deployment should use a production WSGI server and disable debug mode.

## 11. Conclusion

The project demonstrates the main components of a small database-backed banking interface: Flask routes, server-rendered templates, MySQL queries, and stored-procedure-based operations. Completing the database script, adding automated tests, and implementing security controls would be necessary steps before broader use.
