
from flask import Flask, render_template, request
from database import get_connection

app = Flask(__name__)


# =====================================================
# DATABASE HELPER FUNCTIONS
# =====================================================

def fetch_data(sql, params=()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(sql, params)
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def execute_procedure(sql, params=()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(sql, params)

        results = []

        while True:
            if cursor.with_rows:
                results.extend(cursor.fetchall())

            if not cursor.nextset():
                break

        conn.commit()
        return results

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def get_total_bank_balance():
    result = fetch_data("""
        SELECT COALESCE(SUM(balance), 0) AS bank_balance
        FROM ACCOUNT
    """)

    return result[0]["bank_balance"]


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/")
def dashboard():

    customers = fetch_data("""
        SELECT COUNT(*) AS total
        FROM CUSTOMER
    """)

    accounts = fetch_data("""
        SELECT COUNT(*) AS total
        FROM ACCOUNT
    """)

    total_balance = get_total_bank_balance()

    recent_transactions = fetch_data("""
        SELECT
            transaction_id,
            account_id,
            transaction_type,
            amount,
            transaction_date
        FROM `TRANSACTION`
        ORDER BY transaction_date DESC
        LIMIT 10
    """)

    return render_template(
        "dashboard.html",
        total_customers=customers[0]["total"],
        total_accounts=accounts[0]["total"],
        total_balance=total_balance,
        transactions=recent_transactions
    )


# =====================================================
# CUSTOMERS - CREATE AND VIEW
# =====================================================

@app.route("/customers", methods=["GET", "POST"])
def customers():

    message = ""

    if request.method == "POST":

        try:
            name = request.form["customer_name"].strip()
            phone = request.form.get("phone", "").strip()
            address = request.form.get("address", "").strip()
            deposit = float(request.form["deposit"])

            if not name:
                raise ValueError("Customer name is required.")

            if deposit < 0:
                raise ValueError("Opening deposit cannot be negative.")

            execute_procedure(
                "CALL create_customer_account(%s, %s, %s, %s)",
                (name, phone, address, deposit)
            )

            message = "Customer account created successfully!"

        except Exception as e:
            message = f"Error: {e}"

    rows = fetch_data("""
        SELECT
            c.customer_id,
            c.customer_name,
            c.phone,
            a.account_id,
            a.balance
        FROM CUSTOMER c
        JOIN ACCOUNT a
            ON c.customer_id = a.customer_id
        ORDER BY c.customer_id DESC
    """)

    return render_template(
        "customers.html",
        message=message,
        rows=rows
    )


# =====================================================
# ALL BANK ACCOUNTS
# =====================================================

@app.route("/accounts")
def accounts():

    rows = fetch_data("""
        SELECT
            a.account_id,
            c.customer_name,
            c.phone,
            a.balance
        FROM ACCOUNT a
        JOIN CUSTOMER c
            ON a.customer_id = c.customer_id
        ORDER BY a.account_id DESC
    """)

    return render_template(
        "accounts.html",
        rows=rows
    )


# =====================================================
# DEPOSIT MONEY
# =====================================================

@app.route("/deposit", methods=["GET", "POST"])
def deposit():

    message = ""
    current_balance = None
    account_id = ""
    amount = ""

    if request.method == "POST":

        try:
            account_id = int(request.form["account_id"])
            amount = float(request.form["amount"])

            if account_id <= 0:
                raise ValueError("Enter a valid account ID.")

            if amount <= 0:
                raise ValueError("Deposit amount must be greater than zero.")

            execute_procedure(
                "CALL deposit_money(%s, %s)",
                (account_id, amount)
            )

            result = fetch_data(
                "SELECT get_account_balance(%s) AS balance",
                (account_id,)
            )

            current_balance = result[0]["balance"]

            message = "Money deposited successfully!"

        except Exception as e:
            message = f"Error: {e}"

            # Try to retrieve the customer's balance
            try:
                if account_id:
                    result = fetch_data(
                        "SELECT get_account_balance(%s) AS balance",
                        (account_id,)
                    )
                    current_balance = result[0]["balance"]
            except Exception:
                current_balance = None

    total_bank_balance = get_total_bank_balance()

    return render_template(
        "deposit.html",
        message=message,
        current_balance=current_balance,
        total_bank_balance=total_bank_balance,
        account_id=account_id,
        amount=amount
    )


# =====================================================
# WITHDRAW MONEY
# =====================================================

@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():

    message = ""
    current_balance = None
    account_id = ""
    amount = ""

    if request.method == "POST":

        try:
            account_id = int(request.form["account_id"])
            amount = float(request.form["amount"])

            if account_id <= 0:
                raise ValueError("Enter a valid account ID.")

            if amount <= 0:
                raise ValueError("Withdrawal amount must be greater than zero.")

            # Check customer's available balance
            result = fetch_data(
                "SELECT get_account_balance(%s) AS balance",
                (account_id,)
            )

            current_balance = result[0]["balance"]

            if amount > current_balance:

                message = "Insufficient customer balance!"

            else:

                execute_procedure(
                    "CALL withdraw_money(%s, %s)",
                    (account_id, amount)
                )

                # Get updated customer balance
                updated = fetch_data(
                    "SELECT get_account_balance(%s) AS balance",
                    (account_id,)
                )

                current_balance = updated[0]["balance"]

                message = "Money withdrawn successfully!"

        except Exception as e:
            message = f"Error: {e}"

            # Try to retrieve the customer's current balance
            try:
                if account_id:
                    result = fetch_data(
                        "SELECT get_account_balance(%s) AS balance",
                        (account_id,)
                    )
                    current_balance = result[0]["balance"]
            except Exception:
                current_balance = None

    # Get updated total bank balance
    total_bank_balance = get_total_bank_balance()

    return render_template(
        "withdraw.html",
        message=message,
        current_balance=current_balance,
        total_bank_balance=total_bank_balance,
        account_id=account_id,
        amount=amount
    )


# =====================================================
# CHECK CUSTOMER BALANCE
# =====================================================

@app.route("/balance", methods=["GET", "POST"])
def balance():

    message = ""
    current_balance = None
    account_id = ""

    if request.method == "POST":

        try:
            account_id = int(request.form["account_id"])

            if account_id <= 0:
                raise ValueError("Enter a valid account ID.")

            result = fetch_data(
                "SELECT get_account_balance(%s) AS balance",
                (account_id,)
            )

            current_balance = result[0]["balance"]

        except Exception as e:
            message = f"Error: {e}"

    total_bank_balance = get_total_bank_balance()

    return render_template(
        "balance.html",
        message=message,
        current_balance=current_balance,
        total_bank_balance=total_bank_balance,
        account_id=account_id
    )


# =====================================================
# TRANSACTION HISTORY
# =====================================================

@app.route("/history", methods=["GET", "POST"])
def history():

    transactions = []
    error = None
    account_id = None
    searched = False

    if request.method == "POST":

        searched = True

        try:
            account_id = int(request.form["account_id"])

            if account_id <= 0:
                raise ValueError("Enter a valid account ID.")

            transactions = execute_procedure(
                "CALL show_transaction_history(%s)",
                (account_id,)
            )

        except Exception as e:
            error = str(e)

    return render_template(
        "history.html",
        transactions=transactions,
        account_id=account_id,
        error=error,
        searched=searched
    )


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)
