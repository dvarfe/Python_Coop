import sys
import socket
import cmd
import threading
import readline


def get_msgs(s):
    while msg := sys.stdin.buffer.readline():
        try:
            s.sendall(msg)
        except ConnectionError:
            return
        print(f'\n{s.recv(1024).rstrip().decode()}\n')


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    server_thread = threading.Thread(target=get_msgs, args=(s,))
    server_thread.start()
    server_thread.join()
