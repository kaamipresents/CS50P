# Random Password Generator

from random import choice, shuffle

def generate_password(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    updatedChars = ""
    for _ in range(length):
        updatedChars += choice(chars)
    updatedChars = list(updatedChars)
    shuffle(updatedChars)   
    password = ''.join(updatedChars)
    return password

def main():
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length <= 0:
                print("Please enter a positive integer.")
                continue
            password = generate_password(length)
            print(f"Generated password: {password}")
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

main()