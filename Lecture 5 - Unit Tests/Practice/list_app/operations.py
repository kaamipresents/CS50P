def get_last_item(items):
    if not items:
        return None
    return items[-1]

def main():
    items = [1, 2, 3, 4, 5]
    last_item = get_last_item(items)
    print(f"The last item in the list is: {last_item}")

if __name__ == "__main__":
    main