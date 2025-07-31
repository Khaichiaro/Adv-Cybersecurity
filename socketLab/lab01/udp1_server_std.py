import math
import sys
import socket

SERVER_IP = '127.0.0.1'
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
    print(f'[<<<] Receiving message: {msg} from {c_addr}')
    
    client_port = c_addr[1]
    vowels = "aeiouAEIOU"
    vowel_count = sum(1 for char in msg if char in vowels)
    b_number = math.ceil(client_port * 0.03356 - 918.41)
    m_number = b_number + vowel_count
    res = str(m_number)

    s_socket.sendto(res.encode(), c_addr)
    print(f'[>>>] Sending YOUR MAIC NUMBER is: {res} to {c_addr}')
    
s_socket.close()