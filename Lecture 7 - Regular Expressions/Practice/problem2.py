# Extract First Word

import re
text = "Game is very powerful"
# Regular expression to find the first word in the text
pattern = r'\w+'
# Search for the pattern in the text
match = re.search(pattern, text)
if match:
    print("First word:", match.group())
else:
    print("No word found")