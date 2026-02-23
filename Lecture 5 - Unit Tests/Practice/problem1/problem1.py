import math

def calculate_factorial(value):
    """
    Handles the conversion to integer, validation, 
    and factorial calculation.
    """
    try:
        # 1. Convert the passed input to an integer
        number = int(value)
        
        # 2. Check if the number is non-negative
        if number < 0:
            return "Error: Factorial is not defined for negative numbers."
        
        # 3. Use the math library for the calculation
        result = math.factorial(number)
        return f"The factorial of {number} is {result}"
            
    except ValueError:
        return "Error: Invalid input! Please provide a valid whole number."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    # --- Execution ---
    user_provided_input = input("Enter a non-negative integer: ")
    output = calculate_factorial(user_provided_input)
    print(output)