
# ==========================================
# Expense Tracker - Input Module
# Commit 2: Validate and Save Multiple Expenses
# ==========================================

import csv
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


# ==========================================
# 1. Basic Settings
# ==========================================

DATA_FILE = Path(__file__).resolve().parent / "expenses.csv"

FIELDNAMES = ["date", "amount", "category", "notes"]


# ==========================================
# 2. Input Date with Validation
# ==========================================

def input_date():

    while True:
        raw_date = input(
            "Enter date (YYYY-MM-DD, Enter for today): "
        ).strip()

        if not raw_date:
            return date.today().isoformat()

        try:
            if (
                len(raw_date) != 10
                or raw_date[4] != "-"
                or raw_date[7] != "-"
            ):
                raise ValueError

            expense_date = date.fromisoformat(raw_date)

            return expense_date.isoformat()

        except ValueError:
            print("Invalid date! Please use YYYY-MM-DD.")


# ==========================================
# 3. Input Amount with Validation
# ==========================================

def input_amount():

    while True:
        raw_amount = input("Enter amount: ").strip()

        try:
            amount = Decimal(raw_amount)

            if not amount.is_finite() or amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return format(amount, "f")

        except InvalidOperation:
            print("Invalid amount! Please enter a number.")


# ==========================================
# 4. Input Category with Validation
# ==========================================

def input_category():

    while True:
        category = input("Enter category: ").strip()

        if category:
            return category

        print("Category cannot be empty.")


# ==========================================
# 5. Input Optional Notes
# ==========================================

def input_notes():

    return input("Enter notes (optional): ").strip()


# ==========================================
# 6. Collect Expense Information
# ==========================================

def collect_expense():

    expense = {
        "date": input_date(),
        "amount": input_amount(),
        "category": input_category(),
        "notes": input_notes()
    }

    return expense


# ==========================================
# 7. Save Expense to CSV
# ==========================================

def save_expense(expense):

    file_has_data = (
        DATA_FILE.exists()
        and DATA_FILE.stat().st_size > 0
    )

    # Check existing CSV header before appending
    if file_has_data:
        with DATA_FILE.open(
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.reader(file)
            existing_header = next(reader, None)

        if existing_header != FIELDNAMES:
            raise ValueError(
                "CSV format does not match the required columns. "
                "Please check expenses.csv."
            )

    # Append expense to CSV
    with DATA_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        # Write header only for a new or empty file
        if not file_has_data:
            writer.writeheader()

        writer.writerow(expense)


# ==========================================
# 8. Display Expense Information
# ==========================================

def display_expense(expense):

    print("\n" + "=" * 40)
    print("       EXPENSE INFORMATION")
    print("=" * 40)

    print(f"Date     : {expense['date']}")
    print(f"Amount   : {expense['amount']}")
    print(f"Category : {expense['category']}")
    print(f"Notes    : {expense['notes']}")

    print("=" * 40)


# ==========================================
# 9. Ask Whether to Continue
# ==========================================

def ask_continue():

    while True:
        choice = input(
            "\nAdd another expense? (y/n): "
        ).strip().lower()

        if choice in ["y", "yes"]:
            return True

        elif choice in ["n", "no"]:
            return False

        print("Please enter y or n.")


# ==========================================
# 10. Main Program
# ==========================================

def main():

    print("=" * 40)
    print("          EXPENSE TRACKER")
    print("=" * 40)

    saved_count = 0

    while True:

        print("\nPlease enter expense information.")

        expense = collect_expense()

        try:
            save_expense(expense)

            saved_count += 1

            print("\nExpense saved successfully!")

            display_expense(expense)

        except (OSError, ValueError) as error:

            print(f"\nUnable to save expense: {error}")
            break

        if not ask_continue():
            break

    print("\n" + "=" * 40)
    print("         SESSION SUMMARY")
    print("=" * 40)

    print(f"Total expenses added: {saved_count}")
    print(f"Data saved to: {DATA_FILE}")

    print("=" * 40)


# ==========================================
# Program Entry Point
# ==========================================

if __name__ == "__main__":
    main()
