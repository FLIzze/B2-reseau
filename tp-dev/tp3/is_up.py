import os
from sys import argv

case = os.system(f"ping -c1 {argv[1]} 2> /dev/null > /dev/null")
if (case == 0): 
	print("UP !")
else:
	print("DOWN")
