"""Expense Tracker - Member A: interactive input and CSV storage.

Only the Python standard library is required for this module.
"""

import csv
import os
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "expenses.csv"
FIELDNAMES = ["date", "amount", "category", "notes"]

# ANSI colors are optional. VS Code's integrated terminal supports them.
COLOR_ENABLED = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def color(text, code):
    if not COLOR_ENABLED:
        return str(text)
    return f"\033[{code}m{text}\033[0m"


def divider():
    print(color("─" * 56, "36"))


def header():
    print()
    print(color("╔" + "═" * 54 + "╗", "1;36"))
    print(color("║" + "  EXPENSE TRACKER  ·  DAILY SPENDING".ljust(54) + "║", "1;36"))
    print(color("║" + "  Enter • Save • Understand your expenses".ljust(54) + "║", "36"))
    print(color("╚" + "═" * 54 + "╝", "1;36"))


def section(title):
    print()
    divider()
    print(color(f"  {title}", "1;34"))
    divider()


def input_date():
    today = date.today().isoformat()
    while True:
        raw = input(f"  Date [YYYY-MM-DD, Enter = {today}]: ").strip()
        if not raw:
            return today
        try:
            if (len(raw) != 10 or raw[4] != "-" or raw[7] != "-"
                    or not (raw[:4] + raw[5:7] + raw[8:]).isdigit()):
                raise ValueError
            return date.fromisoformat(raw).isoformat()
        except ValueError:
            print(color("  ! Invalid date. Example: 2026-11-22", "33"))


def input_amount():
    while True:
        raw = input("  Amount: ").strip()
        try:
            amount = Decimal(raw)
            if not amount.is_finite() or amount <= 0:
                print(color("  ! Amount must be a positive number.", "33"))
                continue
            return format(amount, "f")
        except InvalidOperation:
            print(color("  ! Please enter a valid numeric amount.", "33"))


def input_category():
    print(color("  Ideas: Food / Transport / Shopping / Entertainment / Other", "90"))
    while True:
        category = input("  Category: ").strip()
        if category:
            return category
        print(color("  ! Category cannot be empty.", "33"))


def input_notes():
    return input("  Notes [optional]: ").strip()


def collect_expense():
    return {
        "date": input_date(),
        "amount": input_amount(),
        "category": input_category(),
        "notes": input_notes(),
    }


def save_expense(expense):
    has_data = DATA_FILE.exists() and DATA_FILE.stat().st_size > 0
    if has_data:
        with DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            header_row = next(csv.reader(file), None)
        if header_row != FIELDNAMES:
            raise ValueError("Existing expenses.csv has a different column layout.")

    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not has_data:
            writer.writeheader()
        writer.writerow(expense)


def read_expenses():
    """Read saved rows for the optional history and summary screens."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in FIELDNAMES):
            raise ValueError("CSV columns do not match date,amount,category,notes.")
        return list(reader)


def show_receipt(expense):
    print()
    print(color("  ✓ Saved successfully!", "1;32"))
    print(f"    Date     : {expense['date']}")
    print(f"    Amount   : {Decimal(expense['amount']):,.2f}")
    print(f"    Category : {expense['category']}")
    print(f"    Notes    : {expense['notes'] or '—'}")


def add_expenses(session):
    while True:
        section(f"NEW EXPENSE  /  ENTRY #{session['count'] + 1}")
        expense = collect_expense()
        try:
            save_expense(expense)
        except (OSError, ValueError) as error:
            print(color(f"  ✗ Could not save: {error}", "1;31"))
            return

        session["count"] += 1
        session["total"] += Decimal(expense["amount"])
        show_receipt(expense)
        while True:
            another = input("\n  Add another expense? [y/n]: ").strip().lower()
            if another in ("y", "yes"):
                break
            if another in ("n", "no", ""):
                return
            print(color("  ! Please enter y or n.", "33"))


def show_history():
    section("RECENT EXPENSES")
    try:
        expenses = read_expenses()
    except (OSError, ValueError) as error:
        print(color(f"  ! Unable to read CSV: {error}", "33"))
        return
    if not expenses:
        print("  No saved expenses yet. Choose 1 to add your first one.")
        return
    for idx, expense in enumerate(reversed(expenses[-8:]), start=1):
        print(f"  {idx:>2}. {expense['date']}  |  {expense['category']}")
        print(f"      Amount: {expense['amount']}    Notes: {expense['notes'] or '—'}")
    print(color(f"\n  Showing latest {min(8, len(expenses))} of {len(expenses)} records", "90"))


def show_category_totals():
    section("CATEGORY SUMMARY")
    try:
        expenses = read_expenses()
    except (OSError, ValueError) as error:
        print(color(f"  ! Unable to read CSV: {error}", "33"))
        return
    totals = defaultdict(Decimal)
    valid_count = 0
    for item in expenses:
        try:
            amount = Decimal(item["amount"])
            category = item["category"].strip()
            if not amount.is_finite() or amount <= 0 or not category:
                continue
        except (InvalidOperation, TypeError):
            continue
        totals[category] += amount
        valid_count += 1
    if not totals:
        print("  No valid expense records yet.")
        return
    for category, amount in sorted(totals.items(), key=lambda item: -item[1]):
        print(f"  • {category}: {amount:,.2f}")
    divider()
    print(color(f"  Total spent: {sum(totals.values()):,.2f}  ({valid_count} records)", "1;32"))


def menu():
    section("MAIN MENU")
    print("  [1]  Add expense")
    print("  [2]  View recent expenses")
    print("  [3]  View category summary")
    print("  [0]  Exit")
    return input("\n  Choose an option [0-3]: ").strip()


def main():
    session = {"count": 0, "total": Decimal("0")}
    header()
    try:
        while True:
            choice = menu()
            if choice == "1":
                add_expenses(session)
            elif choice == "2":
                show_history()
            elif choice == "3":
                show_category_totals()
            elif choice == "0":
                break
            else:
                print(color("  ! Please choose 0, 1, 2, or 3.", "33"))
    except (KeyboardInterrupt, EOFError):
        print("\n  Session interrupted.")
    section("SESSION SUMMARY")
    print(f"  Entries added : {session['count']}")
    print(f"  Amount added  : {session['total']:,.2f}")
    print(f"  CSV location  : {DATA_FILE}")
    print(color("\n  Thank you for using Expense Tracker!", "1;36"))


if __name__ == "__main__":
    main()
