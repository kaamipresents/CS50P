import sys

if len(sys.argv) < 2:
    print("Too Few Arguments")
    sys.exit()

# without slice
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    print(f"Hello, {arg}!")

# with slice
for arg in sys.argv[1:]:
    print(f"Hello, {arg}!")