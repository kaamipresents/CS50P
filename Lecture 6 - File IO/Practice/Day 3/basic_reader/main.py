# Problem 1

def main():
 # basic reader
    with open("employees.csv") as file:
        users = file.readlines()
        print(users)
        total_salary = 0
        for user in users[1:]:
            user = user.strip().split(",")
            if user[2] == "IT":
                print(user)
                total_salary += int(user[3])
        print(f"Total salary for IT employees: {total_salary}")
    

if __name__ == "__main__":
    main()