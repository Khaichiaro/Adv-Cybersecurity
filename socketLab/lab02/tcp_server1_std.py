import sys
import socket

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

print(s1)
print(s_client)

while True:
    msg = s_client.recv(2048)
    if not msg:
        print('QUIT signals from: {addr_client[0]}')
        break
    msg = msg.decode()
    print(f'[<<<] Receiving message: {msg} from {addr_client}')
    msg = msg.upper()
    s_client.sendall(msg.encode())
    print(f'[>>>] Sending response: {msg} to {addr_client}')

s_client.close()
s1.close()
print(f'[*] TCP Server socket closed')