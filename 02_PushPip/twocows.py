import argparse
import random
from cowsay import cowsay, list_cows, read_dot_cow, Option
import sys
import os

parser = argparse.ArgumentParser(
    prog=os.path.basename(sys.argv[0]),
    description="Generates an ASCII image of two cows having a dialogue",
)

parser.add_argument(
    "-e",
    type=str,
    help="An eye string. This is ignored if a preset mode is given",
    dest="eyes",
    default=Option.eyes,
    metavar="eye_string",
)
parser.add_argument(
    "-f", type=str, metavar="cowfile",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)
parser.add_argument(
    "-l", action="store_true",
    help="Lists all cows in the cow path and exits"
)
parser.add_argument(
    "-n", action="store_false",
    help="If given, text in the speech bubble will not be wrapped"
)
parser.add_argument(
    "-T", type=str, dest="tongue",
    help="A tongue string. This is ignored if a preset mode is given",
    default=Option.tongue, metavar="tongue_string"
)
parser.add_argument(
    "-W", type=int, default=40, dest="width", metavar="column",
    help="Width in characters to wrap the speech bubble (default 40)",
)

group = parser.add_argument_group(
    title="Mode",
    description="There are several out of the box modes "
                "which change the appearance of the cow. "
                "If multiple modes are given, the one furthest "
                "down this list is selected"
)
group.add_argument("-b", action="store_const", const="b", help="Borg")
group.add_argument("-d", action="store_const", const="d", help="dead")
group.add_argument("-g", action="store_const", const="g", help="greedy")
group.add_argument("-p", action="store_const", const="p", help="paranoid")
group.add_argument("-s", action="store_const", const="s", help="stoned")
group.add_argument("-t", action="store_const", const="t", help="tired")
group.add_argument("-w", action="store_const", const="w", help="wired")
group.add_argument("-y", action="store_const", const="y", help="young")

parser.add_argument(
    "--random", action="store_true",
    help="If provided, picks a random cow from the COWPATH. "
         "Is superseded by the -f option",
)

parser.add_argument(
    "message_1", default=None, nargs='?',
    help="First message to include in the speech bubble. "
         "If not given, stdin is used instead."
)

parser.add_argument(
    "message_2", default="I can't read input from stdin", nargs='?',
    help="Second message to include in the speech bubble. "
)

def get_preset(args):
    return (
            args.y or args.w or args.t or args.s
            or args.p or args.g or args.d or args.b
    )

def get_cowfile(cow):
    if cow is not None and len(cow.split(os.sep)) > 1:
        with open(cow, "r") as f:
            return read_dot_cow(f)
    else:
        return None

def run(func):
    args = parser.parse_args()

    if args.l:
        print("\n".join(list_cows()))
        return

    if args.message_1 is None:
        args.message_1 = sys.stdin.read()

    if args.random:
        cow = args.f or random.choice(list_cows())
    else:
        cow = args.f or "default"

    first_cow = func(
        message=args.message_1,
        cow=cow,
        preset=get_preset(args),
        eyes=args.eyes,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.n,
        cowfile=get_cowfile(args.f),
    )
    first_cow = first_cow.split('\n')
    second_cow = func(
        message=args.message_2,
        cow=cow,
        preset=get_preset(args),
        eyes=args.eyes,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.n,
        cowfile=get_cowfile(args.f),
    )
    second_cow = second_cow.split('\n')

    first_cow_w = max([len(i) for i in first_cow])
    first_cow_h = len(first_cow) 

    cows_united = [(' ' * (first_cow_w - len(i[0]))).join(map(str, i)) for i in zip(first_cow, second_cow)]
    cows_united = '\n'.join(cows_united)

    print(cows_united)

run(cowsay)