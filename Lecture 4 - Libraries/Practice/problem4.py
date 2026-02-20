from sys import argv

def main():
    if len(argv) != 2:
        print("Usage: python problem4.py <name1>")
        return
    try:
        print(f"Hello, {argv[1]}!")
    except ValueError:
        print("Please provide valid names.")
        return

main()