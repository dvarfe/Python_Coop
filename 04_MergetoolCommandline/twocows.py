import os
import shlex
import cmd
from cowsay import list_cows, make_bubble, THOUGHT_OPTIONS, Bubble, Option, Option, cowsay, cowthink


class twocows(cmd.Cmd):
    prompt = 'moo>> '

    def do_EOF(self, args):
        return 1

    def do_list_cows(self, arg):
        '''
        List all cows in paths from arguments
        If no path specified lists cows from default directory
        '''
        paths = shlex.split(arg)
        for path in paths:
            if not os.path.isdir(path):
                print(f'{path} is incorrect path')
            else:
                print('\n'.join(list_cows(path)))
        if len(arg) == 0:
            print('\n'.join(list_cows()))

    def do_make_bubble(self, args):
        '''
        Makes text bubble. Has 4 arguments.
        text
        brackets=cowsay, -b - defines brackets to wrap text. Accepts 'cowsay' or 'cowthink'
        width=40, -w
        wrap-text=True, -r - whether wrap text or not. 
        '''
        args_parsed = shlex.split(args)
        if len(args_parsed) == 0 or args_parsed[0][0] == '-':
            print('No text specified!')
            return

        text = args_parsed[0]
        brackets = THOUGHT_OPTIONS['cowsay']
        width = 40
        wrap_text = True
        argit = iter(args_parsed)
        next(argit)

        for arg in argit:
            match arg:
                case '-b' | '--brackets':  brackets = THOUGHT_OPTIONS[next(argit).lower()]
                case '-w' | '--width':  width = int(next(argit))
                case '-r' | '--wrap-text':
                    wrap_str = next(argit)
                    wrap_text = bool(wrap_str.lower() ==
                                     'true' or wrap_str == '1')

            print(make_bubble(text, brackets, width, wrap_text))

    def __parse_cowsay(self, cow_args, mode):

        cow_text = cow_args[0]
        cow_name = 'default'
        cow_eyes = Option.eyes
        cow_tongue = Option.tongue
        if len(cow_args) > 1:
            cow_name = cow_args[1]

            eyes_template, tongue_template = 'eyes=', 'tongue='

            for word in cow_args[2::]:
                if word.startswith(eyes_template):
                    cow_eyes = word[len(eyes_template)::]
                elif word.startswith(tongue_template):
                    cow_tongue = word[len(tongue_template)::]

        if mode == 'say':
            return cowsay(message=cow_text, cow=cow_name,
                          eyes=cow_eyes, tongue=cow_tongue)
        if mode == 'think':
            return cowthink(message=cow_text, cow=cow_name,
                            eyes=cow_eyes, tongue=cow_tongue)

    def __unite_cows_aligned(self, first_cow_in, second_cow_in):

        first_cow = first_cow_in.split('\n')
        second_cow = second_cow_in.split('\n')

        first_cow_w = max([len(i) for i in first_cow])
        first_cow_h = len(first_cow)
        second_cow_h = len(second_cow)

        first_cow = ['' for i in range(
            max(first_cow_h, second_cow_h) - first_cow_h)] + first_cow
        second_cow = ['' for i in range(
            max(first_cow_h, second_cow_h) - second_cow_h)] + second_cow

        cows_united = [(' ' * (first_cow_w - len(i[0]))).join(map(str, i))
                       for i in zip(first_cow, second_cow)]
        cows_united = '\n'.join(cows_united)

        return cows_united

    def do_cowsay(self, args):
        '''
        Similar to the cowsay command. 
        cowsay msg [cow_name [parameter=value …]] reply answer [cow_name [[parameter=value …]]

        cow_name - valid .cow file name
        parameter - 'eyes' or 'tongue'
        '''
        parsed_args = shlex.split(args)
        if len(parsed_args) < 3:
            print('Please enter full conversation')
            return
        if 'reply' not in parsed_args:
            print('No reply!')
            return
        reply_begidx = parsed_args.index('reply')
        cow_1 = self.__parse_cowsay(parsed_args[0:reply_begidx], 'say')
        cow_2 = self.__parse_cowsay(parsed_args[reply_begidx + 1:], 'say')

        print(self.__unite_cows_aligned(cow_1, cow_2))

    def complete_cowsay(self, text, line, begidx, endidx):
        words = (line + ".").split()
        cow_list = list_cows()
        text_begin = words[-1][:-1:]
        completion_dict = [c for c in cow_list if c.startswith(text_begin)]
        if (len(words) != 3):
            completion_dict = []
        if 'reply' in words:
            reply_idx = words.index('reply')
            if (len(words) == reply_idx + 3):
                completion_dict = [
                    c for c in cow_list if c.startswith(text_begin)]
        if (len(completion_dict) == 1):
            if text != text_begin:
                completion_idx = text_begin.rfind(text)
                completion_dict = [completion_dict[0][completion_idx::]]
        return completion_dict

    def do_cowthink(self, args):
        '''
        Similar to the cowthink command. 
        cowthink msg [cow_name [parameter=value …]] reply answer [cow_name [[parameter=value …]]

        cow_name - valid .cow file name
        parameter - 'eyes' or 'tongue'
        '''
        parsed_args = shlex.split(args)
        if len(parsed_args) < 3:
            print('Please enter full conversation')
            return
        if 'reply' not in parsed_args:
            print('No reply!')
            return
        reply_begidx = parsed_args.index('reply')
        cow_1 = self.__parse_cowsay(parsed_args[0:reply_begidx], mode='think')
        cow_2 = self.__parse_cowsay(
            parsed_args[reply_begidx + 1:], mode='think')

        print(self.__unite_cows_aligned(cow_1, cow_2))

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.complete_cowsay(text, line, begidx, endidx)


if __name__ == '__main__':
    twocows().cmdloop()
