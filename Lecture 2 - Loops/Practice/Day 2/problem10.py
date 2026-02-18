# Company Payroll Processing System

employees = [
    {"name": "Ali", "salary": 30000},
    {"name": "Sara", "salary": 45000},
    {"name": "Ahmed", "salary": 38000},
    {"name": "Zara", "salary": 52000}
]

def view_salaries():
    print("Employee Salaries Before Increment:")
    for emp in employees:
        print(f"Employee: {emp['name']}, Salary: ${emp['salary']}")

def increment_salaries():
    print("Employee Salaries After Increment:")
    for emp in employees:
        emp['incremented_salary'] = int(emp['salary'] * 1.12) # Simulate incrementing salaries by 12%
        if emp['incremented_salary'] > 60000:
            print(f"Employee: {emp['name']} has a salary above $60,000 after increment. Stopping")
            break
        print(f"Employee: {emp['name']}, Salary: ${emp['incremented_salary']}")

def rerun_payroll():
    while True:
        response = input("Do you want to run the payroll again? (yes/no): ").strip().lower()
        if response == "yes":
            return True
        elif response == "no":
            print("Exiting the program. Goodbye!")
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue
        

def main():
    print("Welcome to the Company Payroll System")
    while True:        
        print("\nMenu:")
        print("1. View Employee Salaries Before Increment")
        print("2. View Employee Salaries After Increment")
        print("3. Exit")

        try:
            choice = int(input("Please enter your choice (1, 2, or 3): "))
            if choice == 1:
                view_salaries()
                if rerun_payroll():
                    continue
                else:
                    break
            elif choice == 2:
                increment_salaries()
                if rerun_payroll():
                    continue
                else:
                    break
            elif choice == 3:
                response = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                if response == "yes":
                    print("Exiting the program. Goodbye!")
                    break
                else:
                    print("Returning to the main menu.")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")
main()