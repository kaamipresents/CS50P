# write a program that shuffles a list of names
from random import shuffle

def main():
    names = ["Ali", "Ahmed", "Sara", "John", "Emily"]
    print("Original list:", names)
    shuffle(names)
    print("Shuffled list:", names)

main()