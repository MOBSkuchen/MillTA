import io
import sly.yacc
from sly import Parser
import sly
from lexer import PLexer
from errors import warning, EmptyFile, InvalidToken, CodeSnippet
from ast_nodes import *


def get_position(p):
    return getattr(p, 'index', -1), getattr(p, 'index', -1) + len(getattr(p, 'value')), getattr(p, 'lineno', 0)


@property
def __repl_val(self):
    for tok in self._slice:
        if isinstance(tok, sly.yacc.YaccSymbol):
            continue
        index = getattr(tok, 'value', None)
        if index is not None:
            return index
    raise AttributeError('No index attribute found')


sly.yacc.YaccProduction.value = __repl_val


# (getattr(p, 'index', -1), getattr(p, 'index', -1) + len(getattr(p, 'value')), getattr(p, 'lineno', 0))
class MutedLogger(object):
    def __init__(self, f):
        self.f = f

    def debug(self, msg, *args, **kwargs):
        self.f.write((msg % args) + '\n')

    info = debug

    def warning(self, msg, *args, **kwargs):
        # Disable this
        pass# warning(msg % args)

    @staticmethod
    def error(self, token, *args):
        if token:
            lineno = getattr(token, 'lineno', 0)
            index = getattr(token, 'index', -1)
            end = index + len(getattr(token, 'value'))
            if lineno:
                InvalidToken(CodeSnippet(self.code, lineno, index, end))()
            else:
                InvalidToken(CodeSnippet(self.code, -1, index, end))()
        else:
            EmptyFile()()

    critical = debug


Parser2 = Parser
Parser2.log = MutedLogger(None)
Parser2.error = Parser2.log.error


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable,PyPep8Naming,PyMethodMayBeStatic,PyRedeclaration
class PParser(Parser2):
    tokens = PLexer.tokens
    precedence = (
        ('nonassoc', NE, LT, LE, GT, GE, EQEQ),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE)
    )

    def __init__(self, code: io.FileIO):
        self.code = code
        self.ast = ModuleNode([], 0)

    @_("statements")
    def body(self, p):
        self.ast.body = p.statements

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('statements statement')
    def statements(self, p):
        p.statements.append(p.statement)
        return p.statements

    @_('RETURN expr')
    def statement(self, p):
        return ReturnNode(p.expr, get_position(p))

    @_('RETURN')
    def statement(self, p):
        return ReturnNode(None, get_position(p))

    @_('DEF name LPAREN def_params RPAREN COLON name  statements SEMI_COLON')
    def statement(self, p):
        return FuncDefNode(p.name0, p.name1, p.statements, p.def_params, get_position(p))

    @_('name COLON name EQ expr')
    def statement(self, p):
        return AssignmentNode(p.name0, p.expr, p.name1, get_position(p))

    @_('name LPAREN params RPAREN')
    def statement(self, p):
        return FuncCallNode(p.name, p.params, get_position(p))

    @_('def_params COMMA def_param COLON name')
    def def_params(self, p):
        p.def_params.append((p.def_param, p.name))
        return p.def_params

    @_('def_param COLON name')
    def def_params(self, p):
        return [(p.def_param, p.name)]

    @_('')
    def def_params(self, p):
        return []

    @_('name')
    def def_param(self, p):
        return p.name

    @_('')
    def def_param(self, p):
        return

    @_('params COMMA param')
    def params(self, p):
        p.params.append(p.param)
        return p.params

    @_('param')
    def params(self, p):
        return [p.param]

    @_('expr')
    def param(self, p):
        return p.expr

    @_('')
    def param(self, p):
        return

    @_('NAME')
    def name(self, p):
        return NameNode(p.NAME, get_position(p))

    @_('name LPAREN params RPAREN')
    def expr(self, p):
        return FuncCallNode(p.name, p.params, get_position(p))

    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr MOD expr',
       'expr GT expr',
       'expr GE expr',
       'expr LT expr',
       'expr LE expr',
       'expr NE expr',
       'expr EQEQ expr',)
    def expr(self, p):
        return ExpressionNode(p[1], p.expr0, p.expr1, get_position(p))

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('name')
    def expr(self, p):
        return p.name

    @_('NUMBER')
    def expr(self, p):
        return DataNode("int", int(p.NUMBER), get_position(p))

    @_('MINUS NUMBER')
    def expr(self, p):
        return DataNode("int", int(p.NUMBER) * -1, get_position(p))

    @_('FLOAT')
    def expr(self, p):
        return DataNode("float", float(p.FLOAT), get_position(p))

    @_('MINUS FLOAT')
    def expr(self, p):
        return DataNode("float", float(p.FLOAT) * -1, get_position(p))

    @_('STRING')
    def expr(self, p):
        return DataNode("string", p.STRING, get_position(p))

    def do_parse(self, tokens):
        self.parse(tokens)
        return self.ast
