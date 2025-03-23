import sys
import socket
import cmd
import threading
import readline
import time

# message structure: [num]:[text]


def get_msgs(cmd, s):
    while msg := s.recv(1024):
        print(f'\n{msg.rstrip().decode()}')
        print(f'{cmd.prompt}{readline.get_line_buffer()}', end='', flush=True)


class Client(cmd.Cmd):
    prompt = 'moo>>'

    def __init__(self, s):
        self.s = s
        super().__init__()
        print(self.s)

    def __send_command(self, command, args):
        self.s.sendall((command + ' ' + args + '\n').encode())

    def do_quit(self, args):
        self.__send_command('quit', args)
        return 1

    def do_yield(self, args):
        self.__send_command('yield', args)

    def do_login(self, args):
        self.__send_command('login', args)

    def do_cows(self, args):
        self.__send_command('cows', args)

    def do_who(self, args):
        self.__send_command('who', args)


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cmdline = Client(s)
    server_thread = threading.Thread(target=get_msgs, args=(cmdline, s))
    server_thread.start()
    cmdline.cmdloop()
    server_thread.join()
