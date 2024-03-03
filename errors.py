import io

from rich import get_console
import sys
from os_flags import *


def clear_scr() -> int: return sys.stdout.write('\033[2m')


console = get_console()


def sys_exit(num, *, lc=False):
    try:
        console.print(f"Exited with code [bold]{num}[/]")
        if not lc:
            sys.exit(num)
        else:
            exit(num)
    except:
        sys.exit(num)


def unknown_error(msg, num=-1, crit=True):
    console.print(f'[dark_red]UNKNOWN SYSTEM ERROR[/]: {msg}')
    console.print(f'If this issue keeps appearing, please open an issue on github')
    if crit:
        sys_exit(num)


def warning(msg):
    if get_bool_flag("ALERTS"): console.print(f'[LIGHT_YELLOW]WARNING[/] : [MAGENTA]{msg}[/]')


class Error:
    # prog_error should always be True, because if it is not, then CodeError should be used
    def __init__(self, num: int, name: str, message: str, causes: list[str] = None, solutions: list[str] = None,
                 prog_error: bool = True, critical: bool = False) -> None:
        self.message = message
        self.causes = causes
        self.solutions = solutions
        self.prog_error = prog_error
        self.num = num
        self.name = name
        self.critical = critical

    def _mk_solutions(self, MSG: str) -> str:
        if self.solutions is not None:
            MSG += "[green underline]Possible solutions[/]:\n"
            for solution in self.solutions:
                MSG += "  --  " + solution + "\n"
        return MSG

    def _mk_causes(self, MSG: str) -> str:
        if self.causes is not None:
            MSG += f"\n"
            MSG += "[red underline]Possible causes[/]:\n"
            for cause in self.causes:
                MSG += "  --  " + cause + "\n"
        return MSG

    def _mk_message(self) -> str:
        MSG = "[dark_red]"
        if self.prog_error:
            MSG += f'PROGRAM '
        MSG += "ERROR[/] | "
        MSG += f"[red]{self.name}[/] [{self.num}] : {self.message}"
        return MSG

    def format(self) -> str:
        MSG = self._mk_message()
        MSG = self._mk_causes(MSG)
        MSG = self._mk_solutions(MSG)
        return MSG

    def __call__(self, *args, **kwargs):
        console.print(self.format())
        if self.critical:
            sys_exit(self.num)


def readlines(f):
    for i in f.readlines():
        if i.endswith("\n"):
            i = i#[:-1]
        yield i


class CodeSnippet:
    def __init__(self, code: io.FileIO, line: int, start: int, end: int) -> None:
        self.code = code
        self.code.seek(0)
        self.line = line - 1
        self.lines = list(readlines(self.code))
        self.acc = self._acc(self.lines[:self.line])
        self.start = start - self.acc
        self.end = end - self.acc
        self.f_line = self.lines[self.line]
        self.snippet = self.f_line[self.start:self.end]

    def _acc(self, lines):
        acc = 0
        for i in lines:
            acc += len(i)
        return acc

    def format(self):
        # This could lead to errors (TODO)
        x = ["-----------------------"]
        if self.line - 1 > -1:
            x.append((f'[dim]{self.line - 1} | [/]' + self.lines[self.line - 1]).replace("\n", ""))
        x.append((f'[bold]{self.line}[/] | ' + "[on yellow]" + self.f_line[:self.start] + "[bold on red]" +
                 self.snippet + "[/]" + self.f_line[self.end:] + "[/]").replace("\n", ""))
        if not (self.line + 1 > len(self.lines) - 1):
            x.append((f'[dim]{self.line + 1} | [/]' + self.lines[self.line + 1] + "").replace("\n", ""))
        x.append("-----------------------")
        render = "\n".join(x)
        return render


class CodeError(Error):
    def __init__(self, num: int, code_snippet: CodeSnippet, name: str, message: str, causes: list[str] = None,
                 solutions: list[str] = None,
                 prog_error: bool = False, critical: bool = False) -> None:
        self.code_snippet = code_snippet
        super().__init__(num, name, message, causes, solutions, prog_error, critical)

    def format(self) -> str:
        MSG = self._mk_message() + "\n"
        MSG += self.code_snippet.format()
        MSG = self._mk_causes(MSG)
        MSG = self._mk_solutions(MSG)
        return MSG[:-1]


class SuppliedError(Error):
    def __init__(self, filename: str):
        super().__init__(num=4, name="Supplied file error",
                         message=f"'{filename}' is not a valid file path!",
                         causes=[f"The file '{filename}' was not found, or can not be accessed"],
                         solutions=["Supply a valid file path"],
                         prog_error=True, critical=True)


class TooManyArguments(Error):
    def __init__(self, num_arguments: int):
        super().__init__(num=5, name="Too many arguments",
                         message=f"Received {num_arguments} extra arguments, but expected fewer",
                         causes=["Too many arguments were received during parsing the arguments",
                                 "The parser could attribute no usage to the arguments"],
                         solutions=["See how many arguments are needed and provide them",
                                    f"View signatures using '[bold]{get_flag("PROG_NAME")} --help[/]'"],
                         prog_error=True, critical=True)


class TooFewArguments(Error):
    def __init__(self, num_arguments: int, expected_arguments: int):
        super().__init__(num=6, name="Too few arguments",
                         message=f"Received only {num_arguments} arguments, but expected {expected_arguments}",
                         causes=["Too few arguments were received during parsing the arguments"],
                         solutions=["See how many arguments are needed and provide them",
                                    f"View signatures using '[bold]{get_flag("PROG_NAME")} --help[/]'"],
                         prog_error=True, critical=True)


class FlagMissingValue(Error):
    def __init__(self, flag_name: int):
        super().__init__(num=6, name="Flag missing value",
                         message=f"The flag '{flag_name}' requires a value",
                         causes=["A flag, which required a value did not get one!"],
                         solutions=["Provide the flag with a value",
                                    f"View signatures using '[bold]{get_flag("PROG_NAME")} --help[/]'"],
                         prog_error=True, critical=True)


## CODE ERRORS ##

class IllegalCharacter(CodeError):
    def __init__(self, code_snippet: CodeSnippet):
        super().__init__(num=16, code_snippet=code_snippet, name="Illegal character",
                         message=f"The character '{code_snippet.snippet}' is not a valid character",
                         causes=["The character could not be decoded by the lexer",
                                 "The character has no associated usage"],
                         solutions=["Remove the character"],
                         prog_error=False, critical=True)
