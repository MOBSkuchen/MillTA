class ASTNode:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def __repr__(self):
        return f'{self.name} (at {self.pos})'


class ValueNode(ASTNode):
    def __init__(self, name, value, pos):
        self.value = value
        super().__init__(name, pos)

    def __repr__(self):
        return f'{self.name} : {self.value} (at {self.pos})'


class NameNode(ValueNode):
    def __init__(self, value, pos):
        super().__init__("Name", value, pos)


class ReturnNode(ValueNode):
    def __init__(self, value, pos):
        super().__init__("Return", value, pos)


class DataNode(ValueNode):
    def __init__(self, typ, value, pos):
        self.typ = typ
        super().__init__("Data", value, pos)

    def __repr__(self):
        return f'{self.name} ({self.typ}) : {self.value} (at {self.pos})'


class ExpressionNode(ASTNode):
    def __init__(self, op, lhs, rhs, pos):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        super().__init__("Expression", pos)

    def __repr__(self):
        return f'{self.lhs} {self.op} {self.rhs} (at {self.pos})'


class AssignmentNode(ASTNode):
    def __init__(self, name, value, typ, pos):
        self.name = name
        self.value = value
        self.typ = typ
        super().__init__("Assignment", pos)

    def __repr__(self):
        return f'{self.name} : {self.typ} = {self.value} (at {self.pos})'


class FuncCallNode(ASTNode):
    def __init__(self, name, params, pos):
        self.params = params
        self.pos = pos
        super().__init__(name, pos)

    def __repr__(self):
        return f'{self.name}({", ".join(self.params)}) at {self.pos}'


class FuncDefNode(ASTNode):
    def __init__(self, name, typ, body, def_params, pos):
        self.typ = typ
        self.body = body
        self.def_params = def_params
        super().__init__(name, pos)

    def __repr__(self):
        return f'def {self.name}({", ".join(self.def_params)}) = [...] at {self.pos}'
