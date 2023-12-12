import sys

def ip_config():
    with open('conf.txt', 'r') as file:
        try:
            infos = file.readline()
            if infos.startswith('#'):
                return 0, 0
            info_split = infos.split(',')
            host = info_split[0].split('=')
            port = info_split[1].split('=')
            return host[1], port[1]
        except:
            return 0, 0

def args():
    global host, port
    if len(sys.argv) == 5:
        if sys.argv[1] == '-p' or sys.argv[1] == '--port' and sys.argv[3] == '-a' or sys.argv[3] == 'address':
            port = sys.argv[2]
            host = sys.argv[4]
            return host, port
    else:
        port = 6969
        host = '127.0.0.1'
        return host, port 
