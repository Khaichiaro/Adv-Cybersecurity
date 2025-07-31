import sys
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2222
fam_name = socket.AF_INET

if len(sys.argv) >21:
    if (sys.argv[1].lower() == 'ipv6') and socket.has_ipv6:
        fam_name = socket.AF_INET6
        SERVER_IP = '::'
        fam_name = socket.AF_INET6

s = socket.socket(fam_name, socket.SOCK_STREAM)
print(f'[*] TCP Client is creating socket... {SERVER_IP}:{SERVER_PORT}')
s.connect((SERVER_IP, SERVER_PORT))
print(f'[**] Connected to server at {s.getpeername()}')

while True:
    msg = input('[>>>] Enter your message: ')
    if msg.lower() == 'quit':
        s.sendall(b'')
        print('[*] Exiting client...')
        break
    s.sendall(msg.encode())
    res = s.recv(2048)
    print(f'[<<<] Response from server: {res.decode()}')

s.close()
print(f'[*] TCP Client socket closed')