# def main function to run the calculator
def main():
    # get the user input for one number 
    num = int(input("Enter a number: "))
    # print the result
    print(f"The square of {num} is: {square(num)}")

# square the number 
def square(n):
    return n * n

main()