from random import randint

def get_valid_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:            
            print("Please enter a valid integer.")

def main():
    # Generate a random number between 1 and 100
    while True:
        user = input("Do you want Generate a random number?(yes/no): ").strip().lower()
        if user == "yes":
            num1 = get_valid_number("Enter the first number: ")
            num2 = get_valid_number("Enter the second number: ")
            ranNum = randint(num1, num2)
            print(f"Random number generated: {ranNum}")
        elif user == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")    

main()