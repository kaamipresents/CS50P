# Warehouse Inventory Control

# dictionary to store the inventory of items in a warehouse
inventory = {
    "Laptop": 4,
    "Mouse": 15,
    "Keyboard": 3,
    "Monitor": 2,
    "Printer": 6
}

def check_all_items():
    print("All Items:")
    for item in inventory:
        quantity = inventory[item]
        print(f"{item}: {quantity} units ")

def check_low_stock_items():
    print("Low Stock Items:")
    for item in inventory:
        quantity = inventory[item]
        if quantity < 5:
            print(f"{item}: {quantity} units")

def restock_items():
    print("Restocking Item:")
    item_name = input("Enter the name of the item to restock: ")
    if item_name in inventory:
        try:            
            restock_amount = int(input(f"Enter the quantity to add to '{item_name}': "))
            if restock_amount > 0:
                inventory[item_name] += restock_amount
                print(f"'{item_name}' has been restocked. New quantity: {inventory[item_name]} units")
            else:
                print("Restock amount must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid positive integer.")  
    else:
        print(f"Item '{item_name}' not found in inventory.")

def main():
    while True:
        print("\nWarehouse Inventory Control")
        print("1. Check All Items")
        print("2. Check Low Stock Items")
        print("3. Restock an Item")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            check_all_items()
        elif choice == '2':
            check_low_stock_items()
        elif choice == '3':
            restock_items()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

main()