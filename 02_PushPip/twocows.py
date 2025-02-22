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
    help="An eye string for first cow. This is ignored if a preset mode is given",
    dest="eyes_1",
    default=Option.eyes,
    metavar="eye_1_string",
)

parser.add_argument(
    "-E",
    type=str,
    help="An eye string for second cow. This is ignored if a preset mode is given",
    dest="eyes_2",
    default=Option.eyes,
    metavar="eye_2_string",
)

parser.add_argument(
    "-f", type=str, metavar="cowfile",
    help="Specifies appearance of the first cow "
        "Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)

parser.add_argument(
    "-F", type=str, metavar="cowfile",
    help="Specifies appearance of the second cow "
        "Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)

parser.add_argument(
    "-l", action="store_true",
    help="Lists all cows in the cow path and exits"
)
parser.add_argument(
    "-n", action="store_false",
    help="If given, text in the speech bubble of first cow will not be wrapped"
)
parser.add_argument(
    "-N", action="store_false",
    help="If given, text in the speech bubble of second cow will not be wrapped"
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
    "message_2", default="Mooo?", nargs='?',
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

def unite_cows_aligned(first_cow_in, second_cow_in):
    
    first_cow = first_cow_in.split('\n')
    second_cow = second_cow_in.split('\n')

    first_cow_w = max([len(i) for i in first_cow])
    first_cow_h = len(first_cow)
    second_cow_h = len(second_cow) 


    first_cow = ['' for i in range(max(first_cow_h, second_cow_h) - first_cow_h) ] + first_cow
    second_cow = ['' for i in range(max(first_cow_h, second_cow_h) - second_cow_h) ] + second_cow

    cows_united = [(' ' * (first_cow_w - len(i[0]))).join(map(str, i)) for i in zip(first_cow, second_cow)]
    cows_united = '\n'.join(cows_united)

    return cows_united

def run(func):
    args = parser.parse_args()

    if args.l:
        print("\n".join(list_cows()))
        return

    if args.message_1 is None:
        args.message_1 = sys.stdin.read()

    if args.message_2 is None:
        args.message_2 = "I can't read from stdin"

    if args.random:
        cow_1 = args.f or random.choice(list_cows())
        cow_2 = args.F or random.choice(list_cows())
    else:
        cow_1 = args.f or "default"
        cow_2 = args.F or "default"

    first_cow = func(
        message=args.message_1,
        cow=cow_1,
        preset=get_preset(args),
        eyes=args.eyes_1,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.n,
        cowfile=get_cowfile(args.f),
    )

    second_cow = func(
        message=args.message_2,
        cow=cow_2,
        preset=get_preset(args),
        eyes=args.eyes_2,
        tongue=args.tongue,
        width=args.width,
        wrap_text=args.N,
        cowfile=get_cowfile(args.f),
    )

    print(unite_cows_aligned(first_cow, second_cow))

run(cowsay)