def main():
    try:
        x = int(input("Enter a number: "))
        if even(x):
            print(f"{x} is even.")
        else:
            print(f"{x} is odd.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

def even(n):
    if n % 2 == 0:
        return True
    else:   
        return False

main()