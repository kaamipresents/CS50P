# problem 3
# sales revenue calculator

import csv

def file_reader(file_path):
    # read the file
    with open(file_path, "r") as file:
        print("Sales Revenue Calculator")
        print("------------------------")
        reader = csv.DictReader(file)
        revenue_list = revenue_calculator(reader)
    return revenue_list

def revenue_calculator(reader):
    revenue_list = []
    for row in reader:
        product = row["product"]
        try:
            quantity = int(row["quantity"])
            price = float(row["price"])
            revenue = quantity * price
            revenue_dict = {"product": product, "revenue": revenue}
            revenue_list.append(revenue_dict)
            print(f"{product}: ${revenue:.2f}")
        except ValueError:
            print(f"Invalid price for product '{product}': {row['price']}")
    print("------------------------")
    return revenue_list

def revenue_sorter(revenue_list):   
    sort_revenue = sorted(revenue_list, key=lambda x: x["revenue"], reverse=True)
    print("Products sorted by revenue:")
    for item in sort_revenue[:3]:  # print top 3 products
        print(f"{item['product']}: ${item['revenue']:.2f}")

def main():
    revenue_list = file_reader("sales.csv")
    revenue_sorter(revenue_list)

if __name__ == "__main__":
    main()