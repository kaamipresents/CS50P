raw_comments = ["Great post!", "", "Very helpful.", "   ", "Love the content!", ""]

# Your Task: Complete the line below
clean_comments = [comment for comment in raw_comments if comment.strip()]

print(clean_comments)
# Expected Output: ['Great post!', 'Very helpful.', 'Love the content!']