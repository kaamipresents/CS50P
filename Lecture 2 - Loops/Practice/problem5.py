# Simple ATM Simulation

start_balance = 1000

def main():
    print("Welcome to the ATM!")
    while True:
        try:
            choice = int(input("Please select an option:\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Exit\n"))
            match choice:
                case 1:
                    check_balance()
                case 2:
                    deposit()
                case 3:
                    withdraw()
                case 4:
                    print("Thank you for using the ATM. Goodbye!")
                    break
                case _:
                    print("Invalid option. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def check_balance():
    print(f"Your balance is ${start_balance}.")

def deposit():
    global start_balance
    try:
        amount = float(input("Enter the amount to deposit: "))
        if amount > 0:
            start_balance += amount
            print(f"Successfully deposited ${amount}. Your new balance is ${start_balance}.")
        else:
            print("Deposit amount must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def withdraw():
    global start_balance
    try:
        amount = float(input("Enter the amount to withdraw: "))
        if amount > 0:
            if amount <= start_balance:
                start_balance -= amount
                print(f"Successfully withdrew ${amount}. Your new balance is ${start_balance}.")
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

main()