"""
cli.py — Command-line version of the Hello User App.
Run:  python cli.py
Demonstrates that logic.py works completely independently of Flask.
"""

import logic


def print_banner():
    print("\n" + "=" * 50)
    print("       HELLO USER APP  —  CLI Version")
    print("=" * 50)


def print_menu():
    print("\nWhat would you like to do?")
    print("  [1] Greet me")
    print("  [2] View greeting history")
    print("  [3] Export history to CSV")
    print("  [4] Clear all history")
    print("  [0] Exit")


def cli_greet():
    name = input("\nEnter your name: ").strip()
    success, result, clean_name = logic.record_greeting(name)

    if not success:
        print(f"\n  ❌  Error: {result}")
    else:
        print(f"\n  ✅  {result}")


def cli_view_history():
    greetings = logic.get_all_greetings()

    if not greetings:
        print("\n  No greetings recorded yet.")
        return

    print(f"\n  — Greeting History ({len(greetings)} total) —\n")
    for i, entry in enumerate(greetings, 1):
        print(f"  {i:>3}. [{entry['timestamp']}]  {entry['name']}")
        print(f"       {entry['message']}")


def cli_export_csv():
    path = logic.export_greetings_csv()
    if path:
        print(f"\n  ✅  Exported to: {path}")
    else:
        print("\n  ❌  No data to export, or export failed.")


def cli_clear():
    confirm = input("\n  This will delete ALL greetings. Type YES to confirm: ")
    if confirm.strip().upper() == "YES":
        ok = logic.delete_all_greetings()
        print("  ✅  All greetings cleared." if ok else "  ❌  Failed to clear.")
    else:
        print("  Cancelled.")


def main():
    print_banner()
    print(f"  Total visitors so far: {logic.get_visitor_count()}")

    while True:
        print_menu()
        choice = input("\nChoice: ").strip()

        if choice == "1":
            cli_greet()
        elif choice == "2":
            cli_view_history()
        elif choice == "3":
            cli_export_csv()
        elif choice == "4":
            cli_clear()
        elif choice == "0":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("\n  ⚠  Invalid choice. Please enter 0–4.")


if __name__ == "__main__":
    main()
