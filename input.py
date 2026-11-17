
# ==========================================
# Expense Tracker - Input Module
# Commit 1: Create Expense Input Structure
# ==========================================


# 1. Input Expense Date
def input_date():
    expense_date = input("Enter date (YYYY-MM-DD): ").strip()
    return expense_date


# 2. Input Expense Amount
def input_amount():
    amount = input("Enter amount: ").strip()
    return amount


# 3. Input Expense Category
def input_category():
    category = input("Enter category: ").strip()
    return category


# 4. Input Optional Notes
def input_notes():
    notes = input("Enter notes (optional): ").strip()
    return notes


# 5. Collect All Expense Information
def collect_expense():

    expense = {
        "date": input_date(),
        "amount": input_amount(),
        "category": input_category(),
        "notes": input_notes()
    }

    return expense


# 6. Display Expense Information
def display_expense(expense):

    print("\n" + "=" * 40)
    print("       EXPENSE INFORMATION")
    print("=" * 40)

    print(f"Date     : {expense['date']}")
    print(f"Amount   : {expense['amount']}")
    print(f"Category : {expense['category']}")
    print(f"Notes    : {expense['notes']}")

    print("=" * 40)


# 7. Main Program
def main():

    print("=" * 40)
    print("          EXPENSE TRACKER")
    print("=" * 40)

    expense = collect_expense()

    display_expense(expense)


# Program Entry Point
if __name__ == "__main__":
    main()
