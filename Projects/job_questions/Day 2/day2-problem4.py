fruits = {
    "apple": 50,
    "banana": 20,
    "orange": 30
}

list_of_fruits = fruits.items()

list = [(key,value) for (key,value) in list_of_fruits]

print(list)