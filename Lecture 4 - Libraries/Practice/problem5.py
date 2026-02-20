# Arithmetic CLI Tool

from sys import argv

def main():
    if len(argv) != 4:
        print("Usage: python problem5.py <operation> <num1> <num2>")
        return
    operation = argv[1]
    try:        
        num1 = float(argv[2])
        num2 = float(argv[3])
    except ValueError:
        print("Please provide valid numbers.")
        return
    
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        try:
            result = num1 / num2
        except ZeroDivisionError:
            print("Cannot divide by zero.")

    else:
        print("Invalid operation. Please choose from +, -, *, /.")
        return
    
    print(f"Result: {result}")

main()