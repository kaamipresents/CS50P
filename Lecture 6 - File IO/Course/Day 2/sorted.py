students_list = []

with open("names.csv", "r") as file:
    lines = file.readlines()
    for line in lines:
        name,email,house = line.strip().split(",") # this splits the line into a list of values using the comma as a delimiter
        students_list.append({
            "name": name,
            "email": email,
            "house": house
        })

for student in sorted(students_list, key=lambda x: x["name"]):
    print(student)