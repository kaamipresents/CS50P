# read user names
with open("names.txt", "r") as file:
    # This is reading and sorting
    for line in sorted(file):
        print(line, end="")