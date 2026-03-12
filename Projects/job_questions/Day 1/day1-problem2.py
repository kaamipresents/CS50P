# Create a function that sorts a list and removes all duplicate items from it.

def sort_and_remove_duplicates(lst):
    # Your Task: Complete the line below
    sorted_unique_lst = sorted(set(lst))
    return sorted_unique_lst

# Test the function
input_list = [3, 1, 2, 3, 4, 1, 5]
result = sort_and_remove_duplicates(input_list)
print(result)  # Output: [1, 2, 3, 4, 5]