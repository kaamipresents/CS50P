# Login & Account Balance System

"""
Data available
"""
username = "admin"
password = "1234"
max_attempts = 3
transactions = [500, -200, 1000, -150, -300]
# transactions = []

def login():
    attempts = 0
    while attempts < max_attempts:
        user_input = input("Enter username: ")
        pass_input = input("Enter password: ")
        if user_input == username and pass_input == password:
            print("Login successful!")
            return True
        else:
            attempts += 1
            print(f"Invalid credentials. Attempts left: {max_attempts - attempts}")
    print("Maximum login attempts reached. Access denied.")

def main():
    if login():
        for i, transaction in enumerate(transactions):
            print(f"Transaction {i+1}: ${transaction}")
    else:
        print("Current balance: $0")

main()