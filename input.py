
import csv
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


# ==========================================
# 1. Basic Settings
# ==========================================

# CSV file will be saved in the same folder as input.py
DATA_FILE = Path(__file__).resolve().parent / "expenses.csv"

# Standard CSV column names
FIELDNAMES = ["date", "amount", "category", "notes"]


# ==========================================
# 2. Input Date
# ==========================================

def input_date():
    today = date.today().isoformat()

    while True:
        raw_date = input(
            f"Date (YYYY-MM-DD, Enter for today {today}): "
        ).strip()

        if not raw_date:
            return today

        try:
            parsed_date = datetime.strptime(
                raw_date, "%Y-%m-%d"
            ).date()

            return parsed_date.isoformat()

        except ValueError:
            print("Invalid date! Please use YYYY-MM-DD.")


# ==========================================
# 3. Input Amount
# ==========================================

def input_amount():
    while True:
        raw_amount = input("Amount: ").strip()

        try:
            amount = Decimal(raw_amount)

            if amount.is_finite() and amount > 0:
                return format(amount, "f")

            print("Amount must be greater than zero.")

        except InvalidOperation:
            print("Invalid amount! Please enter a number.")


# ==========================================
# 4. Input Category
# ==========================================

def input_category():
    while True:
        category = input("Category: ").strip()

        if category:
            return category

        print("Category cannot be empty.")


# ==========================================
# 5. Input Notes
# ==========================================

def input_notes():
    return input("Notes (optional): ").strip()


# ==========================================
# 6. Save Expense to CSV
# ==========================================

def save_expense(expense):

    file_exists = (
        DATA_FILE.exists()
        and DATA_FILE.stat().st_size > 0
    )

    with DATA_FILE.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        # Write header only when creating a new file
        if not file_exists:
            writer.writeheader()

        writer.writerow(expense)


# ==========================================
# 7. Ask Whether to Continue
# ==========================================

def ask_continue():

    while True:
        choice = input(
            "Add another expense? (y/n): "
        ).strip().lower()

        if choice in ["y", "yes", "是"]:
            return True

        elif choice in ["n", "no", "否"]:
            return False

        print("Please enter y or n.")


# ==========================================
# 8. Main Program
# ==========================================

def main():

    print("=" * 40)
    print("       EXPENSE TRACKER")
    print("=" * 40)

    saved_count = 0

    while True:

        print("\nPlease enter expense information.")

        expense = {
            "date": input_date(),
            "amount": input_amount(),
            "category": input_category(),
            "notes": input_notes()
        }

        try:
            save_expense(expense)

            saved_count += 1

            print("\nExpense saved successfully!")
            print(f"Date: {expense['date']}")
            print(f"Amount: {expense['amount']}")
            print(f"Category: {expense['category']}")

        except OSError as error:
            print(f"Unable to save expense: {error}")
            break

        if not ask_continue():
            break

    print("\n" + "=" * 40)
    print(f"Total expenses added: {saved_count}")
    print(f"Data saved to: {DATA_FILE}")
    print("=" * 40)


if __name__ == "__main__":
    main()
