import sys
import socket

if len(sys.argv) > 2:
    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])
else:
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 1111
    
address = (SERVER_IP, SERVER_PORT)
print(f'Server is: {address}')

# client_bind_addr = (SERVER_IP, 34687)
# client_bind_addr = (SERVER_IP, 59978)
c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# c_socket.bind(client_bind_addr)
print(f'[*] UDP Client is creating socket for server {address}')

while True:
    msg = input('[>>>] Enter your msg: ')
    if msg == 'quit':
        c_socket.sendto(b'', address)
        break
    c_socket.sendto(msg.encode(), address)
    res, s_addr = c_socket.recvfrom(2048)
    print(f'[<<<] Response from the server: {res.decode()}')
    # print(f'[<<<] Response from the server: {address}')