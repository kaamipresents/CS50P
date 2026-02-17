"""
Correct password = "python123"
User gets only 3 attempts
If correct → "Login successful"
If 3 wrong attempts → "Account Locked"
"""
correct_password = "python123"
attempts = 0
while attempts < 3:
    password = input("Enter your password: ")
    if password == correct_password:
        print("Login successful")
        break
    else:
        attempts += 1
        print("Incorrect password. Try again.")
    if attempts == 3:
        print("Account Locked")
        break
    