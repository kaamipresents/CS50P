# opening a file
file = open("names.txt", "r")

# read a file
print(file.read(),end="") # this reads the file and moves the cursor to the end of the file

# this is used to move the cursor to the beginning of the file
file.seek(0)

list = file.readlines()
for line in list:
    print(line, end="")

print("Done")

# close a file
file.close()