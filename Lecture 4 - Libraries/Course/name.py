from sys import argv

# This program will ask the user for their name and greet them
def main():
    try:
        name = argv[1]
        print(f"Hello, {name}!")
    except IndexError as e:
        print("Usage: python name.py [name] is missing.")

main()