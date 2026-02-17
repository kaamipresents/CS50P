# HTTP Status Code Interpreter
# Write a program that takes an HTTP status code as input and prints out the corresponding message. Use the following mapping:

def main():
    try:
        status_code = int(input("Enter an HTTP status code: "))
        match status_code:
            case 200:
                print("OK")
            case 201:
                print("Created")
            case 301:
                print("Moved Permanently")
            case 400:
                print("Bad Request")
            case 401:
                print("Unauthorized")
            case 403:
                print("Forbidden")
            case 404:
                print("Not Found")
            case 500:
                print("Internal Server Error")
            case _:
                print("Unknown Status Code")
    except ValueError:
        print("Invalid input. Please enter a valid integer status code.")

main()