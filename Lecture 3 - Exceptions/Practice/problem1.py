# Safe Division Calculator

def get_valid_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    while True:
        try:
            numerator = get_valid_number("Enter first number: ")
            denominator = get_valid_number("Enter second number: ")
            result = numerator / denominator
            print(f"Result: {result}")
            break
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed.")

main()