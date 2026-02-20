# Professional Grade CLI Math Tool

import sys, math

valid_operations = ["add", "subtract", "multiply", "divide", "power", "sqrt", "factorial", "log"]

def main():
    if len(sys.argv) < 3:
        print("Usage: Too Few Arguments. Please provide numbers for the operation.")
        return
    
    operation = sys.argv[1]
    if operation not in valid_operations:
        print("Invalid operation. Please choose from add, subtract, multiply, divide, power, sqrt, factorial, log.")
        return
    elif operation in ["add", "subtract", "multiply", "divide", "power"]:
        if len(sys.argv) < 4:
            print("Usage: Too Few Arguments. Please provide two numbers for the operation.")
            return
        try:        
            num1 = float(sys.argv[2])
            num2 = float(sys.argv[3])
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "power":
                result = math.pow(num1, num2)
            elif operation == "divide":
                try:
                    result = num1 / num2
                except ZeroDivisionError:
                    print("Cannot divide by zero.")
                    return
            print(f"Result: {result}")
        except ValueError:
            print("Please provide valid numeric numbers.")
            return
                
    elif operation in ["sqrt", "factorial", "log"]:
        if len(sys.argv) > 3:
            print("Too Many Arguments for the selected operation. Please provide only one number.")
            return
        try:        
            num1 = float(sys.argv[2])
            if operation == "sqrt":
                if num1 < 0:
                    raise ValueError("Negative numbers are not allowed in square root.")
                result = math.sqrt(num1)
            elif operation == "factorial":
                if not num1.is_integer() or num1 < 0:
                    print("Factorial is only defined for non-negative integers.")
                    return
                result = math.factorial(int(num1))
            elif operation == "log":
                if num1 <= 0:
                    raise ValueError("Negative numbers are not allowed in logarithm.")
                result = math.log(num1)
            else:
                print("Invalid operation. Please choose from add, subtract, multiply, divide, power, sqrt, factorial, log.")
                return
            print(f"Result: {result}")
        except ValueError:
            print("Please provide a valid numeric number.")
            return


if __name__ == "__main__":
    main()