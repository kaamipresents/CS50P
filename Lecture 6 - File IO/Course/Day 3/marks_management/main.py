# Student Marks Management

import csv

def display_student_details():
    print("\nStudent Details:")
    with open("students.csv", "r", newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            print(f"Name: {row[0]}, Math: {row[1]}, Science: {row[2]}, English: {row[3]}")
            total = int(row[1]) + int(row[2]) + int(row[3])
            average = total / 3
            print(f"{row[0]} -> Total: {total} -> Average: {average:.2f}\n")
        print("Student details displayed successfully.")

def get_student_details():
    name = input("Enter student name: ")
    try:
        math = int(input("Enter student math marks: "))
        science = int(input("Enter student science marks: "))
        english = int(input("Enter student english marks: "))
    except ValueError:
        print("Please enter valid integer marks.")
        return
    # Store the data in a file
    store_student_details(name, math, science, english)

def store_student_details(name, math, science, english):
    with open("students.csv", "a", newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty to write headers
            writer.writerow(["Name", "Math", "Science", "English"])
        writer.writerow([name, math, science, english])
    print("Student details stored successfully.")

def main():
    print("Student Marks Management")
    print("-------------------------")
    print("1. Enter Student Details")
    print("2. Display Student Details")
    print("3. Exit")
    while True:
        try:
            choice = input("Enter your choice (1/2/3): ")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")
            continue
        if choice == '1':
            get_student_details()
        elif choice == '2':
            display_student_details()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":    
    main()