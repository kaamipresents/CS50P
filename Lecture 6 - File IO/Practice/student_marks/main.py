students_list = []

with open("students.csv", "r") as file:
    lines = file.readlines()
    for line in lines[1:]: # this is used to skip the header line
        name, math, english, science = line.strip().split(",")
        student = {"name": name, "total": int(math)+int(english)+int(science)}
        students_list.append(student)

for student in sorted(students_list, key=lambda x: x["total"], reverse=True):
    print(student)