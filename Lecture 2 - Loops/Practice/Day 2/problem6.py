# E-Commerce Cart System

cart_prices = [1200, 450, 800, 3000]

def calculate_total(cart):
    total = 0
    for price in cart:
        total += price
    return total

def discount_applying():
    while True:
        user_input = input("Do you want to apply discount? (yes/no): ").lower()
        if user_input == "yes":
            return 0.1
        elif user_input == "no":
            return 0
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def main():
    sub_amount = calculate_total(cart_prices)
    print(f"Total amount in the cart: ${sub_amount}")
    discount = discount_applying()
    total_amount = sub_amount - (sub_amount * discount)
    print(f"Total amount after discount: ${total_amount}")
    
main()