
def main():
    try:
        while True:
            age = int(input("What is your age? "))
            if age < 1 or age > 120:
                print("Invalid age. Please enter you age again.")
            else:
                print(f"You are {age} years old.")
                break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

main()