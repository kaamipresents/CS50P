# Discount Until Budget Ends

budget = 3000
product_cost = 700
products_purchased = 0
while True:
    if budget >= product_cost:
        budget -= product_cost
        products_purchased += 1
    else:
        break
print(f"Products purchased: {products_purchased}")
print(f"Remaining budget: ₹{budget}")