"""
main.py — CLI entry point for the Smart Expense Tracker.
Handles all user interaction: menus, input prompts, output formatting.
"""

from logic import (
    add_expense,
    get_all_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
    get_summary,
    filter_by_category,
    VALID_CATEGORIES,
)


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_expense_row(expense):
    print(
        f"  [{expense['id']}] "
        f"${expense['amount']:.2f}  |  "
        f"{expense['category']:<15}  |  "
        f"{expense['description']:<30}  |  "
        f"{expense['date']}"
    )


def print_expense_table(expenses):
    if not expenses:
        print("  No expenses found.")
        return
    print(f"\n  {'ID':<5} {'Amount':<10} {'Category':<15} {'Description':<30} {'Date'}")
    print("  " + "-" * 80)
    for expense in expenses:
        print_expense_row(expense)


def print_categories():
    print("\n  Available Categories:")
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"    {i}. {cat}")


# ─────────────────────────────────────────────
#  MENU HANDLERS
# ─────────────────────────────────────────────

def handle_add():
    print_header("ADD NEW EXPENSE")

    amount_str = input("  Enter amount (e.g. 25.50): $").strip()
    print_categories()
    category = input("  Enter category: ").strip()
    description = input("  Enter description: ").strip()

    try:
        expense = add_expense(amount_str, category, description)
        print(f"\n  ✅ Expense added successfully! ID: {expense['id']}")
    except ValueError as e:
        print(f"\n  ❌ Error: {e}")
    except RuntimeError as e:
        print(f"\n  ❌ Storage error: {e}")


def handle_view_all():
    print_header("ALL EXPENSES")
    try:
        expenses = get_all_expenses()
        print_expense_table(expenses)
    except RuntimeError as e:
        print(f"\n  ❌ Storage error: {e}")


def handle_view_by_id():
    print_header("VIEW EXPENSE BY ID")
    try:
        expense_id = int(input("  Enter expense ID: ").strip())
        expense = get_expense_by_id(expense_id)
        if expense:
            print_expense_table([expense])
        else:
            print(f"  ❌ No expense found with ID {expense_id}.")
    except ValueError:
        print("  ❌ Please enter a valid integer ID.")


def handle_update():
    print_header("UPDATE EXPENSE")
    try:
        expense_id = int(input("  Enter expense ID to update: ").strip())
        expense = get_expense_by_id(expense_id)
        if not expense:
            print(f"  ❌ No expense found with ID {expense_id}.")
            return

        print(f"\n  Current values:")
        print_expense_table([expense])
        print("\n  Leave blank to keep current value.\n")

        new_amount = input(f"  New amount [${expense['amount']}]: $").strip() or None
        print_categories()
        new_category = input(f"  New category [{expense['category']}]: ").strip() or None
        new_description = input(f"  New description [{expense['description']}]: ").strip() or None

        updated = update_expense(expense_id, new_amount, new_category, new_description)
        print(f"\n  ✅ Expense #{expense_id} updated successfully!")
        print_expense_table([updated])
    except ValueError as e:
        print(f"\n  ❌ Error: {e}")
    except RuntimeError as e:
        print(f"\n  ❌ Storage error: {e}")


def handle_delete():
    print_header("DELETE EXPENSE")
    try:
        expense_id = int(input("  Enter expense ID to delete: ").strip())
        expense = get_expense_by_id(expense_id)
        if not expense:
            print(f"  ❌ No expense found with ID {expense_id}.")
            return

        print(f"\n  About to delete:")
        print_expense_table([expense])
        confirm = input("\n  Are you sure? (yes/no): ").strip().lower()

        if confirm == "yes":
            delete_expense(expense_id)
            print(f"  ✅ Expense #{expense_id} deleted.")
        else:
            print("  Deletion cancelled.")
    except ValueError as e:
        print(f"\n  ❌ Error: {e}")
    except RuntimeError as e:
        print(f"\n  ❌ Storage error: {e}")


def handle_summary():
    print_header("SPENDING SUMMARY")
    try:
        summary = get_summary()

        if summary["count"] == 0:
            print("  No expenses recorded yet.")
            return

        print(f"\n  Total Spent:       ${summary['total']:.2f}")
        print(f"  Total Expenses:    {summary['count']}")
        print(f"  Average Expense:   ${summary['average']:.2f}")

        print("\n  ── By Category ──────────────────────────")
        for category, total in sorted(summary["by_category"].items(), key=lambda x: x[1], reverse=True):
            bar_length = int((total / summary["total"]) * 30)
            bar = "█" * bar_length
            print(f"  {category:<15} ${total:<8.2f} {bar}")

        h = summary["highest_expense"]
        print(f"\n  Highest Expense:   ${h['amount']:.2f} — {h['description']} ({h['category']})")

    except RuntimeError as e:
        print(f"\n  ❌ Storage error: {e}")


def handle_filter():
    print_header("FILTER BY CATEGORY")
    print_categories()
    category = input("\n  Enter category to filter: ").strip()

    try:
        results = filter_by_category(category)
        print(f"\n  Results for '{category}':")
        print_expense_table(results)
        if results:
            total = sum(e["amount"] for e in results)
            print(f"\n  Subtotal: ${total:.2f} across {len(results)} expense(s).")
    except ValueError as e:
        print(f"\n  ❌ Error: {e}")
    except RuntimeError as e:
        print(f"\n  ❌ Storage error: {e}")


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

MENU_OPTIONS = {
    "1": ("Add Expense", handle_add),
    "2": ("View All Expenses", handle_view_all),
    "3": ("View Expense by ID", handle_view_by_id),
    "4": ("Update Expense", handle_update),
    "5": ("Delete Expense", handle_delete),
    "6": ("View Summary", handle_summary),
    "7": ("Filter by Category", handle_filter),
    "0": ("Exit", None),
}


def show_menu():
    print_header("SMART EXPENSE TRACKER")
    for key, (label, _) in MENU_OPTIONS.items():
        print(f"  [{key}] {label}")
    print()


def main():
    print("\n  Welcome to the Smart Expense Tracker 💰")

    while True:
        show_menu()
        choice = input("  Select option: ").strip()

        if choice == "0":
            print("\n  Goodbye! Stay on budget. 👋\n")
            break
        elif choice in MENU_OPTIONS:
            _, handler = MENU_OPTIONS[choice]
            handler()
        else:
            print("  ❌ Invalid option. Please choose from the menu.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
