# Dividing two numbers from user input.
def main():
    # Get the first number from the user.
    num1 = float(input("Enter the first number: "))

    # Get the second number from the user.
    num2 = float(input("Enter the second number: "))

    # Check if the second number is zero to avoid division by zero error.
    if num2 == 0:
        print("Error: Cannot divide by zero.")
    else:
        # Perform the division and display the result.
        result = round(num1 / num2)  # Round the result to 2 decimal places.
        print(f"The result of dividing {num1} by {num2} is: {result}")

try:
    main()
except ValueError:
    print("Error: Please enter valid numbers.")