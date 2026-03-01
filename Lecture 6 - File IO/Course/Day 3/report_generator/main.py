import csv

students = {
    "Ali": [78, 85, 90],
    "Sara": [92, 88, 95],
    "Ahmed": [70, 60, 75]
}

with open("report.csv", "w", newline="") as file:
    # print(dir(csv.writer(file)))
    writer = csv.writer(file)
    writer.writerow(["name", "math", "english", "science"])
    for student, marks in students.items():
        writer.writerow([student] + marks)


