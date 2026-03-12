raw_tags = ["python", "  ", "flask", "python", "", "automation", "flask", "   ", "ai"]
print(raw_tags)

# Your Task: Complete the line below
clean_tags = [tag for tag in raw_tags if tag.strip()]
print(clean_tags)
# Expected Output: ['python', 'flask', 'python', 'automation', 'flask', 'ai']

# task 2 => get the unique tags and sort them
unique_sorted_tags = sorted(set(clean_tags))
print(unique_sorted_tags)
# Expected Output: ['ai', 'automation', 'flask', 'python']