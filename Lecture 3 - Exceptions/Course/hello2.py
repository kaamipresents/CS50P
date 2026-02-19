def get_int():
    while True:
        try:
            return int(input("Please enter an integer: ")) 
        except ValueError:
            pass
            
    

def main():
    x = get_int() # This shows the abstracted logic of getting an integer from the user, and handling any exceptions that may arise from invalid input.
    print(f"You entered: {x}")

main()

