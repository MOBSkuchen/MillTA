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


class Error:
    def __init__(self, num: int, name: str, message: str, causes: list[str] = None, solutions: list[str] = None,
                 prog_error: bool = False, critical: bool = False) -> None:
        self.message = message
        self.causes = causes
        self.solutions = solutions
        self.prog_error = prog_error
        self.num = num
        self.name = name
        self.critical = critical

    def format(self) -> str:
        MSG = "[dark_red]"
        if self.prog_error:
            MSG += f'PROGRAM'
        MSG += " ERROR[/] | "
        MSG += f"[red]{self.name}[/] [{self.num}] : {self.message}"
        if self.causes is not None:
            MSG += f"\n"
            MSG += "[red]Possible causes[/]:\n"
            for cause in self.causes:
                MSG += (" " * 12) + "--  " + cause + "\n"
        if self.solutions is not None:
            MSG += "[green]Possible solutions[/]:\n"
            for solution in self.solutions:
                MSG += (" " * 15) + "--  " + solution + "\n"
        return MSG

    def __call__(self, *args, **kwargs):
        console.print(self.format())
        if self.critical:
            sys_exit(self.num)


class SuppliedFileNotFoundError(Error):
    def __init__(self, filename: str):
        super().__init__(num=4, name="Supplied file not found",
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
                         causes=["Too many arguments were received during parsing the arguments"],
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


def unknown_error(msg, num=-1, crit=True):
    console.print(f'[dark_red]UNKNOWN SYSTEM ERROR[/]: {msg}')
    console.print(f'If this issue keeps appearing, please open an issue on github')
    if crit:
        sys_exit(num)


def warning(msg):
    if get_bool_flag("ALERTS"): console.print(f'[LIGHT_YELLOW]WARNING[/] : [MAGENTA]{msg}[/]')
