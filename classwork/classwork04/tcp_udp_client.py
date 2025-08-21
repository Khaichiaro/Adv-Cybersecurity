import sys
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2025

def tcp_connection(port):
    c_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'[*] TCP Client is creating socket... {SERVER_IP}:{port}')
    c_tcp.connect((SERVER_IP, port))
    print(f'[**] Connected to server at {c_tcp.getpeername()}')

    while True:
        msg = input('[>>>] Enter your message: ')
        if msg.lower() == 'quit':
            c_tcp.sendall(b'')
            print('[*] Exiting client...')
            break
        c_tcp.sendall(msg.encode())
        res = c_tcp.recv(2048)
        print(f'[<<<] Response from server: {res.decode()}')

    c_tcp.close()
    print(f'[*] TCP Client socket closed')

def main():
    address = (SERVER_IP, SERVER_PORT)
    print(f'Server is: {address}')

    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'[*] UDP Client is creating socket for server {address}')

    while True:
        msg = input('[>>>] Enter your msg: ')
        if msg.lower() == 'quit':
            c_socket.sendto(b'', address)
            print('[*] Exiting client...')
            break
        c_socket.sendto(msg.encode(), address)
        res, s_addr = c_socket.recvfrom(2048)
        print(f'[<<<] Response from the server: {res.decode()}')

        if res.decode().startswith("Opening TCP connection on port"):
            try:
                port_num = int(res.decode().split()[-1])
                tcp_connection(port_num)
            except Exception as e:
                print(f'[!] Error in TCP connection: {e}')
    c_socket.close()
    print(f'[*] UDP Client socket closed')

if __name__ == "__main__":
     main()
