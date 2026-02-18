# Employee Salary Processing System

def main():
    salaries = [25000, 40000, 32000, 28000, 50000]
    increment = 0.1  # 10% increment
    updated_salaries = []
    for salary in salaries:
        salary += salary * increment  # Apply 10% increment
        updated_salaries.append(salary)
        # print(f"Updated Salary: {salary}")

    # write program to print the updated salaries using while loop
    i = 0
    while i < len(updated_salaries):
        if updated_salaries[i] > 45000:
            break
        print(f"Updated Salary: {updated_salaries[i]}")
        i += 1

main()