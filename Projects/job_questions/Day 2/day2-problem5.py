students = {
    "Ali": 85,
    "Sara": 92,
    "Omar": 78
}

students_list = students.items()

sorted_list = sorted(students_list, key=lambda x: x[1], reverse=True)

list = [(key,value) for (key,value) in sorted_list]

print(list)