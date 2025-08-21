import socket
import sys

SERVER_IP = '0.0.0.0'
SERVER_PORT = 2025

def tcp_connection(port):
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'[*] TCP Server is creating socket... {SERVER_IP}:{port}')
    s_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f'[**] SO_REUSEADDR flag is used')
    s_tcp.bind((SERVER_IP, port))
    print(f'[**] Binding socket to local address')
    s_tcp.listen(100)
    print(f'[***] Listening for client (max: 1) at {s_tcp.getsockname()}')
    s_tcp_client, addr_tcp_client = s_tcp.accept()
    print(f'[<<<] Accepted a connection from {s_tcp_client.getpeername()}')

    print(s_tcp)
    print(s_tcp_client)

    while True:
        msg = s_tcp_client.recv(2048)
        if not msg:
            print(f'===== QUIT signals TCP =====')
            break
        msg = msg.decode()
        print(f'[<<<] Receiving message: {msg} from {addr_tcp_client}')
        msg = msg.upper()
        s_tcp_client.sendall(msg.encode())
        print(f'[>>>] Sending response: {msg} to {addr_tcp_client}')

    s_tcp_client.close()
    s_tcp.close()
    print(f'[*] TCP Server socket closed')

def main():
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
        try:
            port_num = int(msg)
            if(1024 <= port_num <= 65535):
                s_socket.sendto(f"Opening TCP connection on port {port_num}".encode(), c_addr)
                print(f"===== Opending TCP connection on port {port_num} =====")
                tcp_connection(port_num)
                continue
        except ValueError:
            pass
        msg = msg.upper()
        s_socket.sendto(msg.encode(), c_addr)
        print(f'[>>>] Sending message: {msg} to {c_addr}')
    
    s_socket.close()
    print('[*] UDP Server socket closed')

if __name__ == "__main__":
    main()
