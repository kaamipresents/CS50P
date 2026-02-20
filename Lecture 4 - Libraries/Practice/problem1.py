# Advanced Calculator (Using math)
from math import sqrt, pow, factorial, log

def main():
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        if num1 < 0 or num2 < 0:
            print("Please enter non-negative numbers.")
        else:
            while True:
                operation = input("Choose an operation (sqrt, pow, factorial, log): ").strip().lower()
                if operation == "sqrt":
                    num1 = sqrt(num1)
                    num2 = sqrt(num2)
                    print(f"Square root of first number: {num1}")
                    print(f"Square root of second number: {num2}")
                elif operation == "pow":
                    result = pow(num1, num2)
                    print(f"Result: {result}")
                elif operation == "factorial":
                    num1 = factorial(int(num1))
                    num2 = factorial(int(num2)) 
                    print(f"Factorial of second number: {num2}")
                    print(f"Factorial of first number: {num1}")
                elif operation == "log":
                    num1 = log(num1)
                    num2 = log(num2)
                    print(f"Log of second number: {num2}")
                    print(f"Log of first number: {num1}")
                else:
                    print("Invalid operation. Please choose from sqrt, pow, factorial, log.")
                    continue
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

main()