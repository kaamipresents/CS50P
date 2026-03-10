# Find First Price in Text

import re
text = "The laptop costs 75000 rupees"
# Regular expression to find the first price in the text
pattern = r'\d+'    

# Search for the pattern in the text
match = re.search(pattern, text)
if match:
    print("Price found:", match.group())    
else:    
    print("Price not found")