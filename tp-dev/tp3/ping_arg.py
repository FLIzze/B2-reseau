from sys import argv
import os

print(os.system(f"ping -c1 {argv[1]}"))
