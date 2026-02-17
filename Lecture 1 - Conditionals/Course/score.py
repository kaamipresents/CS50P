def main():
    try:
        ## get user score for grading
        score = int(input("Enter your score (0-100): "))
        ## check if score is valid
        if score < 0 or score > 100:
            print("Invalid score. Please enter a score between 0 and 100.")
        else:
            if score >= 90:
                grade = "A"
            elif score >= 80:   
                grade = "B"
            elif score >= 70:
                grade = "C"
            elif score >= 60:
                grade = "D"
            else:
                grade = "F"
            print(f"Your grade is: {grade}") 
    except ValueError:
        print("Invalid input. Please enter a valid integer score.")

main()
