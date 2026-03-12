employees = {
    "E101": "Ahmed",
    "E102": "Hina",
    "E203": "Zeeshan"
}

tuple = employees.items()

list = [(key,value) for (key,value) in tuple]
print(list)

for item in list:
    if item[0].startswith("E10"):
        print(item[0])
