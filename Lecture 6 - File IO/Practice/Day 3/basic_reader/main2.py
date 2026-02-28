# Problem 1a
import csv

def main():
 # basic reader
    with open("employees.csv") as file:
        reader =csv.reader(file)
        total_salary = 0
        it_count = 0
        for row in reader:
            if row[2] == "IT":
                it_count += 1
                print(row)
                total_salary += int(row[3])
        print(f"Total salary for IT employees: {total_salary}")
        print(f"Average salary for IT employees: {total_salary/it_count}")

if __name__ == "__main__":
    main()