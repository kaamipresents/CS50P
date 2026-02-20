# Professional Grade CLI Math Tool

from ast import main
import sys, math

def main():
    if len(sys.argv) < 3:
        print("Usage: Too Few Arguments. Please provide numbers for the operation.")
        return
    elif len(sys.argv) > 3:
        if sys.argv[1] == "add" or sys.argv[1] == "subtract" or sys.argv[1] == "multiply" or sys.argv[1] == "divide" or sys.argv[1] == "power" and len(sys.argv) ==3:
            try:        
                num1 = float(sys.argv[2])
                num2 = float(sys.argv[3])
                if num1 < 0 or num2 < 0:
                    raise ValueError("Negative numbers are not allowed.")
            except ValueError:
                print("Please provide valid numeric numbers.")
                return
    
    operation = sys.argv[1]
    try:        
        num1 = float(sys.argv[2])
        num2 = float(sys.argv[3])
        if num1 < 0 or num2 < 0:
            raise ValueError("Negative numbers are not allowed.")
    except ValueError:
        print("Please provide valid numeric numbers.")
        return

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        try:
            result = num1 / num2
        except ZeroDivisionError:
            print("Cannot divide by zero.")
    elif operation == "power":
        result = math.pow(num1, num2)
    elif operation == "sqrt":
        result = math.sqrt(num1)
    elif operation == "factorial":
        result = math.factorial(num1)
    elif operation == "log":
        result = math.log(num1)
    else:
        print("Invalid operation. Please choose from add, subtract, multiply, divide, power, sqrt, factorial, log.")
        return
    print(f"Result: {result}")

if __name__ == "__main__":
    main()