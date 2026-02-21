import cowsay
from sys import argv

if len(argv) == 2:
    cowsay.trex(f"Hello, {argv[1]}!")