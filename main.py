import sys
from argument_parser import ArgumentParser, Argument, Flag
from os_flags import set_flag
from errors import sys_exit

__version__ = "0.0.1"
EX_FILE_NAME = sys.argv.pop(0)
PROG_NAME = "MillTA"
set_flag("PROG_NAME", PROG_NAME)
set_flag("VERSION", __version__)
ap = None


def main():
    global ap
    ap = ArgumentParser("The MillTA compiler!") \
        .add_help() \
        .add_version() \
        .parse()


if __name__ == '__main__':
    main()
    sys_exit(0)