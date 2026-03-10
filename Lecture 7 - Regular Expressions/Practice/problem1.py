# Detect a Number in Text

# Example Text 
"My order number is 4589"

import re 
text = "My order number is 4589"
# Regular expression to find a number in the text
pattern = r'\d+'
# Search for the pattern in the text
match = re.search(pattern, text)    
if match:
    print("Number found:", match.group())
else:
    print("Number not found")