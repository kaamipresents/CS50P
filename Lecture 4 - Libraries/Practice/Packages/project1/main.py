
from ecommerce import users, products, orders
from ecommerce.utils import logger

# ==============================
# APPLICATION FLOW
# ==============================

def main():
    logger.log_info("Application started")

    user = users.create_user("kami", "kami@email.com")
    product = products.create_product("Laptop", 1500)

    products.apply_discount(product, 10)

    order = orders.create_order(user, product, 2)

    users.display_user(user)
    products.display_product(product)
    orders.display_order(order)

    users.deactivate_user(user)
    logger.log_warning("User has been deactivated")

    users.display_user(user)

    logger.log_info("Application finished")


if __name__ == "__main__":
    main()