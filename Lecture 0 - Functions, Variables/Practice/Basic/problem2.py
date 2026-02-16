# Mini Billing System

# Ask user item price
item_price = float(input("Please enter the price of the item: "))
item_price = item_price.strip()  # Remove any leading/trailing whitespace

# Calculate the tax (assuming a tax rate of 7.5%)
tax_rate = 0.1
tax_amount = item_price * tax_rate
# Calculate the total price
total_price = item_price + tax_amount

# Print the total price
print(f"The total price of the item, including tax, is: ${total_price:,.2f}")