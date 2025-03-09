from cowsay import cowsay, list_cows
import os
import shlex
import cmd


class twocows(cmd.Cmd):
    prompt = 'moo>> '

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


if __name__ == '__main__':
    twocows().cmdloop()
