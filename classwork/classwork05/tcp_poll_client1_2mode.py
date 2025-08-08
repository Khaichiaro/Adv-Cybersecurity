import sys
import socket

if len(sys.argv) == 2:
	SERVER_IP = sys.argv[1]
	SERVER_PORT = int(sys.argv[2])
else:
	SERVER_IP = '127.0.0.1'
	SERVER_PORT = 3333

address = (SERVER_IP, SERVER_PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_client:
	print(f'[*] TCP Client is creating socket for server {address}')
	s_client.connect(address)
	print(f'[**] Connected to Server')

	while True:
		msg = input('[>>>] Enter your message: ').strip()
		if msg == 'quit' or msg == '':
			s_client.sendall(b'')
			break
		elif msg.lower() == 'v':
			s_client.sendall(b'v')
			print('[*] Switched to Viewer Mode. Waiting for messages...')
			while True:
				res = s_client.recv(2048)
				if res:
					print(res.decode())
				else:
					print("[!] Server disconnected")
					s_client.close()
		else:
			s_client.sendall(msg.encode())
			res = s_client.recv(2048)
			print(f'[<<<] Response from the server: {res.decode()}')
