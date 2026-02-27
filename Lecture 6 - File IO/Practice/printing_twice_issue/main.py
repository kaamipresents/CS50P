with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())

    print("---- AGAIN ----")

    file.seek(0)
    for line in file:
        print(line.strip())