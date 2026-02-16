# Custom Greeting Function

def greet(name="User"):
    name = name.strip().title()  # Remove whitespace and convert to title case  
    print(f"Hello, {name}! Welcome to the greeting system.")

# Ask User name
user_name = input("Please enter your name: ")

greet()
greet(user_name)