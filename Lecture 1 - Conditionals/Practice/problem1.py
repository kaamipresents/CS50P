# Simple Calculator (Beginner Level) using match

def main():
    try:
        x = int(input("Enter a number: "))
        y = int(input("Enter another number: "))
        operation = input("Enter an operation (+, -, *, /): ")
        match operation:
            case "+":
                print(f"{x} + {y} = {add(x, y)}")
            case "-":
                print(f"{x} - {y} = {subtract(x, y)}")
            case "*":
                print(f"{x} * {y} = {multiply(x, y)}")
            case "/":
                print(f"{x} / {y} = {divide(x, y)}")
            case _:
                print("Invalid operation. Please enter +, -, *, or /.")
    except ValueError:
        print("Invalid input. Please enter valid integers.")

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

main()