# ATM PIN Verification

def main():
    correct_pin = "4321"
    max_attempts = 3
    while True:
        input_pin = input("Please enter your PIN: ")
        max_attempts -= 1
        if input_pin == correct_pin:
            print("Access Granted.")
            break
        elif max_attempts == 0:
            print("Card Blocked.")
            break
        else:
            print("Incorrect PIN. Please try again.")

main()