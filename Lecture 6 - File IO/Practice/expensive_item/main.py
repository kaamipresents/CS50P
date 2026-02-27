items = []

with open("expenses.csv", "r") as file:
    lines = file.readlines()
    for line in lines[1:]:
        item, category, amount = line.strip().split(",")
        try:
            items.append({
                "item": item,
                "amount": int(amount)
            })
        except ValueError:
            print(f"Invalid amount for item '{item}': {amount}")

print(items)

for item in sorted(items, key=lambda x: x["amount"], reverse=True):
    print(f"{item['item']}: ${item['amount']}")