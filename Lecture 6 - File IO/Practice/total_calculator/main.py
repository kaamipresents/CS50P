items = []
total = {}

with open("expenses.csv", "r") as file:
    lines = file.readlines()
    for line in lines[1:]:
        item, category, amount = line.strip().split(",")
        try:
            items.append({
                "item": item,
                "category": category,
                "amount": int(amount)
            })
            if category not in total:
                total[category] = int(amount)
            else:
                total[category] += int(amount)
        except ValueError:
            print(f"Invalid amount for item '{item}': {amount}")

print(items)
print(total)

for item in sorted(total.items(), key=lambda x: x[1], reverse=True):
    print(f"{item[0]}: ${item[1]}")
