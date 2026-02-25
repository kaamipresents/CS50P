# get user names

for i in range(3):
    with open("names.txt", "a") as file:
        name = input("What's your name? ")
        file.write(name + "\n")