
# ==============================
# PRODUCT MANAGEMENT
# ==============================

def create_product(name, price):
    return {
        "name": name,
        "price": price
    }

def apply_discount(product, percent):
    discount_amount = product["price"] * (percent / 100)
    product["price"] -= discount_amount
    return product

def display_product(product):
    print(f"Product: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print("-" * 30)
