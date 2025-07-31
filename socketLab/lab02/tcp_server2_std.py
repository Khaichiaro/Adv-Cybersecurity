import sys
import socket
import os

SERVER_IP = '0.0.0.0'
SERVER_PORT = 2222

fam_name = socket.AF_INET
if len(sys.argv) > 1:
    if (sys.argv[1].lower() == 'ipv6') and socket.has_ipv6:
        fam_name = socket.AF_INET6
        SERVER_IP = '::'
        fam_name = socket.AF_INET6

s1 = socket.socket(fam_name, socket.SOCK_STREAM)
print(f'[*] TCP Server is creating socket... {SERVER_IP}:{SERVER_PORT}')
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f'[**] SO_REUSEADDR flag is used')
s1.bind((SERVER_IP, SERVER_PORT))
print(f'[**] Binding socket to local address')
s1.listen(100)
print(f'[***] Listening for client (max: 1) at {s1.getsockname()}')
s_client, addr_client = s1.accept()
print(f'[<<<] Accepted a connection from {s_client.getpeername()}')
file_info = s_client.recv(1024).decode()
filename, filesize = file_info.split(':')
filename = os.path.basename('new_' + filename)
filesize = int(filesize)
print(f'File Name: {filename}')
print(f'File Size: {filesize/1024} KB') 

with open (filename, "wb") as f:
    while True:
        read = s_client.recv(2048)
        if not read:
            break
        f.write(read)
        print(f'[>>>] File {filename} received successfully from {addr_client}')

s_client.close()
s1.close()