item_name = input("Please enter the name of the item: ")

try:
    item_price = float(input("Please enter the price of the item: "))
    quantity = int(input("What is the quantity that you want: "))

    if item_price < 0 or quantity < 0:
        print("Price and quantity must be positive numbers.")
    else:
        total = item_price * quantity

        print("\n----- INVOICE -----")
        print(f"Item: {item_name}")
        print(f"Price: ${item_price:.2f}")
        print(f"Quantity: {quantity}")
        print(f"Total: ${total:.2f}")

except ValueError:
    print("Invalid input. Please enter numeric values.")
