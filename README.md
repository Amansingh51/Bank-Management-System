# Bank Management System

A Flask web application for basic bank-account management. The interface is branded as Chandigarh University Bank (CUB) and uses MySQL for customer, account, and transaction data.

## Features

- Dashboard with customer and account totals, bank-wide balance, and recent transactions
- Create a customer with an opening deposit
- View customer and account lists
- Deposit to and withdraw from an account
- Look up an account balance
- View an account's transaction history

## Requirements

- Python 3
- MySQL Server
- The Python packages listed in `requirements.txt`

## Setup

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install the Python dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create a MySQL database named `bank_management_system` and configure the connection using environment variables. For example, in PowerShell:

   ```powershell
   $env:DB_HOST = "localhost"
   $env:DB_USER = "root"
   $env:DB_PASSWORD = "your-mysql-password"
   $env:DB_NAME = "bank_management_system"
   $env:DB_PORT = "3306"
   ```

4. Create the database tables, stored procedures, and function used by the app. The required SQL objects are listed in [Database requirements](#database-requirements). The checked-in `database/bank_management.sql` file is currently empty and does not create them.

5. Start the application:

   ```powershell
   python app.py
   ```

   Open `http://127.0.0.1:5000` in your browser.

To check the MySQL connection and list available tables, run:

```powershell
python test_db.py
```

## Database requirements

The application expects these tables and columns:

- `CUSTOMER`: `customer_id`, `customer_name`, `phone`
- `ACCOUNT`: `account_id`, `customer_id`, `balance`
- `TRANSACTION`: `transaction_id`, `account_id`, `transaction_type`, `amount`, `transaction_date`

It also calls these MySQL routines:

- Procedure `create_customer_account(customer_name, phone, address, opening_deposit)`
- Procedure `deposit_money(account_id, amount)`
- Procedure `withdraw_money(account_id, amount)`
- Procedure `show_transaction_history(account_id)`
- Function `get_account_balance(account_id)`

These are inferred from the SQL statements in `app.py`; their definitions and the database schema are not included in the current SQL file.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | Dashboard |
| `/customers` | Create and list customers |
| `/accounts` | List accounts |
| `/deposit` | Deposit funds |
| `/withdraw` | Withdraw funds |
| `/balance` | Check an account balance |
| `/history` | Search transaction history by account |

## Project layout

```text
.
├── app.py
├── database.py
├── database/
│   └── bank_management.sql
├── templates/
├── requirements.txt
└── test_db.py
```

## Security note

This project is intended as a learning/demo application, not as production banking software. It does not implement user authentication or authorization. Database credentials are read from environment variables; keep passwords in local environment configuration and do not commit secrets.
