
# ==============================
# ORDER MANAGEMENT
# ==============================

def create_order(user, product, quantity):
    total_price = product["price"] * quantity
    return {
        "user": user,
        "product": product,
        "quantity": quantity,
        "total_price": total_price
    }

def display_order(order):
    print(f"User: {order['user']['username']}")
    print(f"Product: {order['product']['name']}")
    print(f"Quantity: {order['quantity']}")
    print(f"Total: ${order['total_price']:.2f}")
    print("=" * 40)

