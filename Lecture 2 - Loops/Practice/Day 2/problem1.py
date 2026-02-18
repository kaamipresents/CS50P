# Ordet total calculator
prices = [1200, 450, 799, 1500, 299]
total = 0
costly_items = []
for price in prices:
    total += price
    if price > 500:
        costly_items.append(price)
print(f"Total cost: ${total}")
print(f"Costly items: {costly_items}")