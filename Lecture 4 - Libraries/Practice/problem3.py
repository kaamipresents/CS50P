# Date Difference Calculator (Using datetime)
from datetime import datetime

def main():
    while True:
        try:
            date_format = "%Y-%m-%d"
            date1_str = input("Enter the first date (YYYY-MM-DD): ")
            date2_str = input("Enter the second date (YYYY-MM-DD): ")
            date1 = datetime.strptime(date1_str, date_format)
            date2 = datetime.strptime(date2_str, date_format)
            difference = abs((date2 - date1).days)
            print(f"The difference between {date1_str} and {date2_str} is {difference} days.")
            break
        except ValueError:
            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
            continue

main()