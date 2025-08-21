import sys
import socket, select
READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

SERVER_IP = '0.0.0.0'
SERVER_PORT = 3333
addr_s = (SERVER_IP, SERVER_PORT)

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f'[*] TCP Server is creating socket... ({SERVER_IP}):{SERVER_PORT}')
s1.setblocking(False)
print(f'[**] Non-blocking mode is enabled')

s1.bind(addr_s)
s1.listen(100)
print(f'[***] Listening for client (max: 10) at {s1.getsockname()}')

socks_dict = {s1.fileno(): s1}
addr_dict = {}
mode_dict = {}

poller = select.poll()
poller.register(s1, READ_ONLY)

while True:
    events = poller.poll()
    print(events)
    for fd, event in events:
        sock = socks_dict[fd]

        if event & (select.POLLIN | select. POLLPRI):
            if sock is s1:
                s_client, address = sock.accept()
                print('==============================')
                print(f'[++] Accepted a new connection from: {s_client.getpeername()}')
                print(f'[++] Sockket FD is: {s_client.fileno()}')
                print('==============================')
                poller.register(s_client, READ_ONLY)
                socks_dict[s_client.fileno()] = s_client
                addr_dict[s_client] = address
                mode_dict[s_client] = "normal"
            else:
                msg = sock.recv(2048)
                if msg:
                    text = msg.decode().strip()
                    print(f'[<<] Receiving message: "{text}" from {addr_dict[sock]} (mode={mode_dict[sock]})')
                    if text.lower() == 'v':
                        mode_dict[sock] = "viewer"
                        sock.sendall(b"*** You are now in Viewer Mode ***")
                        print(f'[!!] Client {addr_dict[sock]} switched to Viewer Mode')
                    else:
                        if mode_dict[sock] == "normal":
                            m = text.upper()
                            sock.sendall(m.encode())
                            print(f'[>>] Sending messagge: {m} to {addr_dict[sock]}')
                            # ส่งข้อความนี้ไปให้ทุก viewer พร้อมแสดง address ของ client ที่ส่ง
                            for cli, mode in mode_dict.items():
                                if mode == "viewer" and cli != sock:
                                    try:
                                        cli.sendall(f"[Viewer Mode] Receiving message:  {m} from {addr_dict[sock]}".encode())
                                    except:
                                        pass
                        else:
                            sock.sendall(b"[Viewer Mode] You cannot send messages.")
                else:
                    print('###############################')
                    print(f'Client {addr_dict[sock]} closed socket normally')
                    poller.unregister(sock)
                    del addr_dict[sock]
                    del socks_dict[fd]
                    print(f'addr_dict: {addr_dict.values()}')
                    print(f'socks_dict: {socks_dict.keys()}')
                    print('##############################')
                    sock.close()
        elif event & select.POLLOUT:
            msg = '=== Socket FD is' + str(sock.fileno())
            sock.sendall(msg.encode())
            poller.modify(sock, READ_ONLY)
            print(f'[>>] Sending message POLLOUT event')
        elif event & (select.POLLHUP | select.POLLERR):
            print(f'Client {addr_dict[sock]} close socket normally')
            poller.unregister(sock)
            del addr_dict[sock]
            del socks_dict[fd]
            sock.close()