users_data = []

with open("sales_data.csv","r") as file:
    sales_data = file.readlines()
    for sale in sales_data[1:]:
        id, name, product, category, quantity, price = sale.strip().lower().split(",")
        user_data = {"id":id, "name":name, "product": product, "category":category, "quantity":quantity, "price":price}
        users_data.append(user_data)

for user in users_data:
    print(f"{user["name"].capitalize()} bought {product}")