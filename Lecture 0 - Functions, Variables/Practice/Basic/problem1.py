# Ask your their full name
full_name = input("Please enter your full name: ")
full_name = full_name.strip()  # Remove any leading/trailing whitespace
full_name = full_name.title()  # Convert to title case (e.g., "john doe" -> "John Doe")

# Greet them with their full name
print(f"Hello, {full_name}! Welcome to the greeting system.")