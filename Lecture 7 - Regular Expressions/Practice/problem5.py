# Detect Email Pattern

import re

text = "Contact me at kami@gmail.com"

# Regular expression to find an email pattern in the text
pattern = r'\w+@\w+\.\w+' 
# Search for the pattern in the text
match = re.search(pattern, text)
if match:
    print("Email found:", match.group())

else:   
    print("Email not found")
