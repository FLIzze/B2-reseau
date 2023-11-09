import os
import socket
from sys import argv
import psutil

def lookup(arg):
    return socket.gethostbyname(arg)

def ping(arg):
    case = os.system(f"ping -c1 {arg} 2> /dev/null > /dev/null")
    if (case == 0):
        return "UP!"
    else:
        return "DOWN!"

def ip():
    ipa_dic = (psutil.net_if_addrs())
    return ipa_dic["wlp4s0"][0][1]

result = ""
if len(argv) == 1:
	result = "utilisez une fonction"
elif len(argv) == 2:
    if argv[1] == 'ip':
        result = ip()
    else:
        result = "il manque un argument"
elif len(argv) == 3:
    if argv[1] == 'ping':
        result = ping(argv[2])
    elif argv[1] == 'lookup':
        result = lookup(argv[2])
    elif argv[1] == 'ip':
        result = "ip n'a pas d'argument"
    else:
        result = f"{argv[1]} n'existe pas"

print(result)
