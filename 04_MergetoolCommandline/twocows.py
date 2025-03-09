from cowsay import list_cows, make_bubble, THOUGHT_OPTIONS, Bubble
import os
import shlex
import cmd


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


if __name__ == '__main__':
    twocows().cmdloop()
