# Detect Extra Spaces


import re

text = "Python   is   powerful"
text2 = "Python is powerful"
# Regular expression to find extra spaces in the text
# Search for the pattern in the text
matches = re.search(r"\s{2,}", text2)
if matches:
    print("Extra spaces found")
else:
    print("No extra spaces found")