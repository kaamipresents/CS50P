def main():
    # Ask user about their details
    name = input("What is your name? ").strip().title()
    item = input("Which item you want to buy? ")

    try:
        price = float(input("What is the price of the item? "))
        if price < 0:
            print("Price cannot be negative")
            exit(1)
            
    except ValueError:
        print("Please Enter Valid Price")

    try:
        quantity = int(input("How many items do you want to buy? "))
        if quantity < 0:
            print("Quantity cannot be negative")
            exit(1)
    except ValueError:
        print("Please Enter Valid Quantity")

    subtotal = price * quantity
    tax = subtotal * 0.07
    total_cost = subtotal + tax

    print("---INVOICE---")
    print(f"Customer name: {name}")
    print(f"Item Purchased: {item}")
    print(f"Price Per Item: {price}")
    print(f"Quantity: {quantity}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Total Cost: ${total_cost:.2f}")
        
main()