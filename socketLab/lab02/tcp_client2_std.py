import sys
import socket
import os 
from time import sleep

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2222
address = (SERVER_IP, SERVER_PORT)

filename = sys.argv[1]
filesize = os.path.getsize(filename)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'[*] TCP Client is creating socket... {SERVER_IP}:{SERVER_PORT}')
s.connect((SERVER_IP, SERVER_PORT))
print(f'[**] Connected to server at {s.getpeername()}')

info = filename + ':' + str(filesize)
s.send(info.encode())
sleep(0.5)  # Wait for server to be ready

with open(filename, "rb") as f:
    while True:
        read = f.read(2048)
        if not read:
            break
        s.sendall(read)
        print(f'[>>>] File {filename} sent successfully to {s.getpeername()}')

s.close()
print(f'[*] TCP Client socket closed')