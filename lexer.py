import io
from sly import Lexer
from errors import IllegalCharacter, CodeSnippet


def group(*choices): return '(' + '|'.join(choices) + ')'


def any(*choices): return group(*choices) + '*'


def maybe(*choices): return group(*choices) + '?'


Hexnumber = r'0[xX](?:_?[0-9a-fA-F])+'
Binnumber = r'0[bB](?:_?[01])+'
Octnumber = r'0[oO](?:_?[0-7])+'
Decnumber = r'(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Exponent = r'[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group(r'[0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?',
                   r'\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = r'[0-9](?:_?[0-9])*' + Exponent


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable,PyPep8Naming,PyMethodMayBeStatic,PyRedeclaration
class PLexer(Lexer):
    def __init__(self, code: io.FileIO):
        self.code = code
        super().__init__()

    tokens = {
        NAME,
        NUMBER,
        STRING,
        FLOAT,
        PLUS,
        MINUS,
        DIVIDE,
        LPAREN,
        RPAREN,
        SEMI_COLON,
        LT,
        LE,
        GT,
        GE,
        EQ,
        EQEQ,
        NE,
        DEF,
        RETURN,
        TIMES,
        COLON,
        MOD,
        COMMA,
    }

    literals = {',', ';'}

    FLOAT = group(Pointfloat, Expfloat)

    NUMBER = group(
        Hexnumber,
        Binnumber,
        Octnumber,
        Decnumber
    )

    ignore = ' \t\r'

    @_(r'\n')
    def newline(self, t):
        self.lineno += 1

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['def'] = DEF
    NAME['return'] = RETURN
    STRING = r'(\".*?\")|(\'.*?\')'
    GE = r'>='
    GT = r'>'
    LE = r'<='
    LT = r'<'
    NE = r'!='
    EQEQ = r'=='
    EQ = r'='
    LPAREN = r'\('
    RPAREN = r'\)'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    COLON = r':'
    SEMI_COLON = r';'

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    def error(self, t):
        IllegalCharacter(CodeSnippet(self.code, t.lineno, t.index, t.index + 1))()
