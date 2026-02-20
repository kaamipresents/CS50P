import random

def main():
    # Generate a random number between 1 and 100
    while True:
        user = input("Do you want to flip a coin? (yes/no): ").strip().lower()
        if user == "yes":
            coin = random.choice(['heads', 'tails'])
            print(coin)
            continue
        elif user == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")    

main()