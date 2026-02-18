# write a program to get user input until user enters positive integer
while True:
    try:
        num = int(input("Please enter a positive integer: "))
        if num > 0:
            print(f"Thank you! You entered {num}.")
            break
        else:
            print("That's not a positive integer. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

for _ in range(num):
    print("Meow")