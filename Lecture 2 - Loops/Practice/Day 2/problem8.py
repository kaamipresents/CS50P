# Employee Performance Analyzer

performance_scores = [75, 82, 90, 60, 88, 55]
def calculate_average(scores):
    total = 0
    for score in scores:
        total += score
    average = total / len(scores)
    return average

def classify_employees(scores):
    average = calculate_average(scores)
    for score in scores:
        if score >= 80:
            print(f"Score of {score}: Good")
        elif score >= 60 and score <= 80:
            print(f"Score of {score}: Average")
        else:
            print(f"Score of {score}: Poor")

def main():
    average_score = calculate_average(performance_scores)
    print(f"Average Performance Score: {average_score:.2f}")
    classify_employees(performance_scores)

main()