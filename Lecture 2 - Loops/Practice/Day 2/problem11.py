# Bank Account Transaction Manager

account = {
    "name": "Ali Khan",
    "balance": 50000
}

transactions = []

def view_account_details():
    print(f"\nAccount Holder: {account['name']}")
    print(f"Current Balance: ${account['balance']}")

def deposit_money():
    try:
        amount = float(input("Enter the amount to deposit: $"))
        if amount > 0:
            account['balance'] += amount
            transactions.append({
                "type": "deposit",
                "amount": amount,
                "balance_after": account['balance']
            })
            print(f"Deposit of ${amount} successful. New balance: ${account['balance']}")
        else:
            print("Deposit amount must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")

def withdraw_money():
    try:
        amount = float(input("Enter the amount to withdraw: $"))    
        if amount > 0 and amount <= account['balance']:
            account['balance'] -= amount
            transactions.append({
                "type": "withdrawal",
                "amount": amount,
                "balance_after": account['balance']
            })
            print(f"Withdrawal of ${amount} successful. New balance: ${account['balance']}")
        else:            
            print("Invalid withdrawal amount. Please enter a positive number that does not exceed your current balance.")  
    except ValueError:        
        print("Invalid input. Please enter a valid amount.")

def view_transaction_history():
    print("\nTransaction History:")
    for transaction in transactions:
        print(transaction)
    print(f"Total Balance: ${account['balance']}")

    
def main():
    while True:
        print("\nWelcome to the Bank Account Transaction Manager")
        print("1. View Account Details")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. View Transaction History")
        print("5. Exit")

        if account['balance'] < 10000:
            print("Warning: Your account balance is below $5000. Please consider depositing more funds to avoid any issues.")

        try:
            choice = int(input("Please enter your choice (1, 2, 3, 4, or 5): "))
            if choice == 1:
                view_account_details()
            elif choice == 2:
                deposit_money()
            elif choice == 3:
                withdraw_money()
            elif choice == 4:
                view_transaction_history()
            elif choice == 5:
                confirmation = input("Are you sure you want to exit? (yes/no): ").lower()
                if confirmation == "yes":
                    print("Thank you for using the Bank Account Transaction Manager. Goodbye!")
                    break
                elif confirmation == "no":                    
                    continue
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")    
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

main()