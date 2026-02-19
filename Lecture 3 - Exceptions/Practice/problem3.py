# Dictionary Key Checker

student = {
    "name": "Ali",
    "age": 22,
    "grade": "A"
}

def main():
    while True:
        key = input("Enter the key to access the student dictionary: ")
        try:
            value = student[key]
            print(f"The value for '{key}' is: {value}")
            break
        except KeyError:
            print(f"Key '{key}' not found in the student dictionary.")

main()