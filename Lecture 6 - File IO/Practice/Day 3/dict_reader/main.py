# Problem 2
import csv

def main():
 # basic reader
    with open("employees.csv") as file:
        reader =csv.DictReader(file)
        for row in sorted(reader, key=lambda x: x["salary"], reverse=True):
            try:
                user_salary = int(row["salary"])
                if user_salary > 65000:
                    print(f"{row['name']} - {user_salary}")
            except ValueError:
                print(f"Invalid salary for {row['name']}: {row['salary']}")

if __name__ == "__main__":
    main()