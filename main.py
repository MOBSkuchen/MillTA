import io
import sys
from argument_parser import ArgumentParser, Argument, Flag
from os_flags import set_flag, set_bool_flag
from errors import sys_exit, SuppliedError, warning
from lexer import PLexer
from rich import get_console

console = get_console()
__version__ = "0.0.1"
EX_FILE_NAME = sys.argv.pop(0)
PROG_NAME = "MillTA"
set_flag("PROG_NAME", PROG_NAME)
set_flag("VERSION", __version__)
ap = None


def try_get_file(filepath) -> io.FileIO:
    try:
        f = open(filepath, 'r')
        if not filepath.endswith('.mta'):
            warning(f"The file '{filepath}' is not a MillTA (.mta) file!")
        return f
    except FileNotFoundError or PermissionError or OSError or UnicodeError:
        SuppliedError(filepath)()


def lex_f(filepath):
    f = try_get_file(filepath)
    lexer = PLexer(f)
    tokens = lexer.tokenize(f.read())
    for token in tokens:
        console.print(f"LINE {token.lineno - 1} [{token.index}-{token.end}] | [bold]{token.type}[/] : {token.value}")
    f.close()


def main():
    global ap
    ap = ArgumentParser("The MillTA compiler!") \
        .add_help() \
        .add_version() \
        .add(Argument("lex", ["filepath"], lex_f, "Lexes a file")) \
        .add(Flag("disable-alerts", "a", None, "DISABLE_ALERTS", "Disables alters (warnings)")) \
        .parse()


if __name__ == '__main__':
    main()
    sys_exit(0)
