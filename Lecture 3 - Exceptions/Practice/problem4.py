# Custom Exception – Age Validator

# Asks the user to enter their age.
# If the age is negative → raise a custom exception.
# If the age is greater than 120 → raise a different custom exception.
# If input is not a number → handle ValueError.
# If age is valid → print:

def main():
    while True:
        try:
            age = int(input("Enter your age: "))
            if age < 0:
                raise ValueError("Age cannot be negative.")
            elif age > 120:
                raise ValueError("Age cannot be greater than 120.")
            else:
                print(f"Your age is: {age}")
                break
        except ValueError as e:
            print(e)

main()