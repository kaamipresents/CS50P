students_list = []

with open("names.csv", "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip() # this removes the newline character at the end of each line
        student_data = line.split(",") # this splits the line into a list of values using the comma as a delimiter
        students_list.append({
            "name": student_data[0],
            "email": student_data[1],
            "hosue": student_data[2]
        })
print(students_list)