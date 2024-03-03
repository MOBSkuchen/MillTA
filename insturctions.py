def base_instr(operation, operand1, operand2):
    return f'{operation} {operand1}, {operand2}'


def mov(destination, source):
    return base_instr('mov', destination, source)


def add(destination, source):
    return base_instr('add', destination, source)


def sub(destination, source):
    return base_instr('sub', destination, source)


def mul(destination, source):
    return base_instr('mul', destination, source)


def cmp(operand1, operand2):
    return base_instr('cmp', operand1, operand2)


def jmp(label):
    return f'jmp {label}'


def call(function):
    return f'call {function}'


def ret():
    return 'ret'


def push(value):
    return f'push {value}'


def pop(destination):
    return f'pop {destination}'


def lea(destination, source):
    return base_instr('lea', destination, source)


def inc(operand):
    return f'inc {operand}'


def dec(operand):
    return f'dec {operand}'
