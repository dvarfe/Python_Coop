import sys
import socket
import cmd
import threading
import readline
import time

# message structure: [num]:[text]

system_messages = {}


def get_msgs(cmd, s):
    while msg := s.recv(8192):
        msg_received = msg.rstrip().decode()
        if msg_received[0:2] == '0:':
            print(f'\n{msg_received[2:]}')
            print(f'{cmd.prompt}{readline.get_line_buffer()}',
                  end='', flush=True)
        else:
            command_num, msg = msg_received.split(':', 1)
            system_messages[int(command_num)] = msg


class Client(cmd.Cmd):
    prompt = 'moo>>'

    def __init__(self, s):
        self.s = s
        self.command_num = 0
        super().__init__()

    def __send_command(self, command, args):
        self.s.sendall((command + ' ' + args + '\n').encode())

    def __get_response(self):
        while True:
            if self.command_num in system_messages:
                return system_messages[self.command_num]

    def __print_answer(self, response):
        print(f'\n{response}')
        print(f'{readline.get_line_buffer()}',
              end='', flush=True)

    def do_quit(self, args):
        self.__send_command('quit', args)
        return 1

    def do_yield(self, args):
        self.__send_command('yield', args)

    def do_login(self, args):
        self.__send_command('login', args)

    def do_cows(self, args):
        self.__send_command('cows', args)
        self.command_num += 1
        cows_avail = self.__get_response()
        self.__print_answer(cows_avail)

    def do_who(self, args):
        self.__send_command('who', args)
        self.command_num += 1
        cows_online = self.__get_response()
        self.__print_answer(cows_online)

    def do_say(self, args):
        self.__send_command('say', args)

    def complete_say(self, text, line, begidx, endidx):
        self.command_num += 1
        self.__send_command('who', '')
        cows_online = self.__get_response().split()
        words = (line + ".").split()
        text_begin = words[-1][:-1:]
        completion_dict = [c for c in cows_online if c.startswith(text_begin)]
        if (len(words) > 3):
            completion_dict = []
        if (len(completion_dict) == 1):
            if text != text_begin:
                completion_idx = text_begin.rfind(text)
                completion_dict = [completion_dict[0][completion_idx::]]
        return completion_dict

    def complete_login(self, text, line, begidx, endidx):
        self.command_num += 1
        self.__send_command('cows', '')
        cows_avail = self.__get_response().split()
        words = (line + ".").split()
        text_begin = words[-1][:-1:]
        completion_dict = [c for c in cows_avail if c.startswith(text_begin)]
        if (len(words) > 3):
            completion_dict = []
        if (len(completion_dict) == 1):
            if text != text_begin:
                completion_idx = text_begin.rfind(text)
                completion_dict = [completion_dict[0][completion_idx::]]
        return completion_dict


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cmdline = Client(s)
    server_thread = threading.Thread(target=get_msgs, args=(cmdline, s))
    server_thread.start()
    cmdline.cmdloop()
    server_thread.join()
