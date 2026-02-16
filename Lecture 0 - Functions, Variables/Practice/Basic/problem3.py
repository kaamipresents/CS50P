# Even/Odd Checker Using Modulo

# Ask user for a number
number = int(input("Please enter a number: "))

# use % operator
if number % 2 == 0:
    print(f"{number} is even.")
else:
    print(f"{number} is odd.")