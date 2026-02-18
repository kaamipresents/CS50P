# Website Traffic Analysis

def main():
    # Simulated website traffic data (number of visitors per day)
    visitors = [120, 340, 560, 230, 800, 150, 400]
    total_visitors = 0
    day_with_most_visitors = 0
    high_traffic_day = 0
    for visitor in visitors:
        total_visitors += visitor
        if visitor > 300:
            day_with_most_visitors += 1
        if visitor > high_traffic_day:
            high_traffic_day = visitor 
        average_visitors = total_visitors / len(visitors)
    print(f"Total visitors: {total_visitors}")
    print(f"High traffic day: {high_traffic_day}")
    print(f"Days with most visitors: {day_with_most_visitors}")
    print(f"Average visitors per day: {average_visitors}")
    

main()