# List Index Access
numbers = [10, 20, 30, 40, 50,90, 100, 110, 120, 130]

def main():
    while True:
        try:
            #enter an index to access the list
            index = int(input("Enter an index to access the list: "))
            print(f"The number at index {index} is: {numbers[index]}")
            break
        except IndexError:
            print(f"Error: Index out of range. Please enter a valid index between 0 and {len(numbers)-1}.")
        except ValueError:
            print("Error: Invalid input. Please enter a valid integer index.")

main()