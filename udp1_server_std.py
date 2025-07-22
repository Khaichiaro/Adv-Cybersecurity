import sys
import socket

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1111
address = (SERVER_IP, SERVER_PORT)

s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_socket.bind(address)
print(f'[*] UDP Server is creating socket... {SERVER_IP}:{SERVER_PORT}')
print(f'[**] Binding socket to local address')

while True:
    msg, c_addr = s_socket.recvfrom(2048)
    if not msg:
        print(f'QUIT!!!')
        break
    msg = msg.decode('utf-8')
    print(f'[<<<] Receiving message: {msg} from {address}')
    msg = msg.upper()
    s_socket.sendto(msg.encode(), c_addr)
    print(f'[>>>] sending message: {msg} to {address}')
    
s_socket.close()