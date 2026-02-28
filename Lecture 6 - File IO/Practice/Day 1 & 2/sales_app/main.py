users_data = []

def data_reading():
    with open("sales_data.csv","r") as file:
        sales_data = file.readlines()
        for sale in sales_data[1:]:
            id, name, product, category, quantity, price = sale.strip().lower().split(",")
            user_data = {"id":id, "name":name, "product": product, "category":category, "quantity":quantity, "price":price}
            users_data.append(user_data)
    print("Sales Data:")
    print("-----------")
    for user in users_data:
        print(f"ID: {user['id']}, Name: {user['name'].capitalize()}, Product: {user['product'].capitalize()}, Category: {user['category'].capitalize()}, Quantity: {user['quantity']}, Price: {user['price']}")

    for user in users_data:
        print(f"{user['name'].capitalize()} bought {user['product']}")

def total_revenue():
    total_revenue = 0
    for user in users_data:
        try:
            quantity = int(user["quantity"])
            price = float(user["price"])
            total_revenue += quantity * price
        except ValueError:
            print(f"Invalid data for user {user['name']}. Skipping this entry.")
    print(f"Total Revenue: ${total_revenue:.2f}")

def most_spending_user():
    user_revenue = {}
    for user in users_data:
        name = user["name"]
        try:
            quantity = int(user["quantity"])
            price = float(user["price"])
            revenue = quantity * price
            if name in user_revenue:
                user_revenue[name] += revenue
            else:
                user_revenue[name] = revenue
        except ValueError:
            print(f"Invalid data for user {user['name']}. Skipping this entry.")
    most_spending = max(user_revenue, key=user_revenue.get)
    print(f"Most Spending User: {most_spending.capitalize()} with ${user_revenue[most_spending]:.2f}")

def revenue_category():
    category_revenue = {}
    for user in users_data:
        category = user["category"]
        try:
            quantity = int(user["quantity"])
            price = float(user["price"])
            revenue = quantity * price
            if category in category_revenue:
                category_revenue[category] += revenue
            else:
                category_revenue[category] = revenue
        except ValueError:
            print(f"Invalid data for user {user['name']}. Skipping this entry.")
    print("Revenue per Category:")
    for category, revenue in category_revenue.items():
        print(f"{category.capitalize()}: ${revenue:.2f}")

def main():
    data_reading()
    total_revenue()
    # revenue per category
    revenue_category()
    most_spending_user()

if __name__ == "__main__":
    main()