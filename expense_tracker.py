"""Personal expense tracker."""

import os
import subprocess  # nosec B404
import tempfile
from datetime import datetime

# Read sync password from environment or use demo fallback
BANK_SYNC_PASSWORD = os.getenv("BANK_SYNC_PASS", "demo-sync-pass")
expenses = []
monthly_budget = 20000  # pylint: disable=invalid-name
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")


def add_expense(amount, category="Misc", note=""):
    """Add an expense entry."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat()
    })
    return True


def total_by_category():
    """Get total spending by category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly budget."""
    global monthly_budget  # pylint: disable=global-statement
    monthly_budget = new_budget


def remaining_budget():
    """Calculate remaining budget."""
    spent = sum(expense["amount"] for expense in expenses)
    return monthly_budget - spent


def biggest_expense():
    """Find the largest expense entry."""
    try:
        return max(expenses, key=lambda expense: expense["amount"])
    except ValueError:
        return None


def print_ledger():
    """Print all logged expenses."""
    for i, expense in enumerate(expenses, 1):
        print(i, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check if bank password matches."""
    return password == BANK_SYNC_PASSWORD


def export_report():
    """Create a temp report file."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", dir=REPORT_DIR, delete=False
    ) as temp_file:
        return temp_file.name


def open_statement(path):
    """Open statement using xdg-open."""
    safe_path = os.path.abspath(path)
    subprocess.run(["xdg-open", safe_path], check=False)  # nosec B603, B607


# Aliases for backward compatibility
addExpense = add_expense  # pylint: disable=invalid-name
totalByCategory = total_by_category  # pylint: disable=invalid-name
setBudget = set_budget  # pylint: disable=invalid-name
remainingBudget = remaining_budget  # pylint: disable=invalid-name
biggestExpense = biggest_expense  # pylint: disable=invalid-name
printLedger = print_ledger  # pylint: disable=invalid-name
checkSyncPassword = check_sync_password  # pylint: disable=invalid-name
exportReport = export_report  # pylint: disable=invalid-name
openStatement = open_statement  # pylint: disable=invalid-name


def main():
    """Run sample demo."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after setBudget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        monthly_budget
    )


if __name__ == "__main__":
    main()
