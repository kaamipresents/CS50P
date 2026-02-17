def main():
    try:
        x = int(input("Enter a number: "))
        y = int(input("Enter another number: "))
        
        if x == y or x < y:
            print(f"{x} is less than or equal to {y}.")
        else:
            print(f"{x} is greater than {y}.")
    except ValueError:
        print("Invalid input. Please enter valid integers.")

main()