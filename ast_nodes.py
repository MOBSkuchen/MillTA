class ASTNode:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def __repr__(self):
        return f'{self.name}'


class ValueNode(ASTNode):
    def __init__(self, name, value, pos):
        self.value = value
        super().__init__(name, pos)

    def __repr__(self):
        return f'{self.name} : {self.value}'


class NameNode(ValueNode):
    def __init__(self, value, pos):
        super().__init__("Name", value, pos)

    def __repr__(self):
        return self.value


class ReturnNode(ValueNode):
    def __init__(self, value, pos):
        super().__init__("Return", value, pos)

    def __repr__(self):
        return f'return {self.value}'


class DataNode(ValueNode):
    def __init__(self, typ, value, pos):
        self.typ = typ
        super().__init__("Data", value, pos)

    def __repr__(self):
        return f'{self.value}: {self.typ}'


class ExpressionNode(ASTNode):
    def __init__(self, op, lhs, rhs, pos):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        super().__init__("Expression", pos)

    def __repr__(self):
        return f'{self.lhs} {self.op} {self.rhs}'


class AssignmentNode(ASTNode):
    def __init__(self, name, value, typ, pos):
        self.name = name
        self.value = value
        self.typ = typ
        super().__init__(name, pos)

    def __repr__(self):
        return f'{self.name}: {self.typ} = {self.value}'


class FuncCallNode(ASTNode):
    def __init__(self, name, params, pos):
        self.params = params
        self.pos = pos
        super().__init__(name, pos)

    def __repr__(self):
        return f'{self.name}({", ".join(map(repr, self.params))}'


class FuncDefNode(ASTNode):
    def __init__(self, name, typ, body, def_params, pos):
        self.typ = typ
        self.body = body
        self.def_params = def_params
        super().__init__(name, pos)

    def __repr__(self):
        return f'def {self.name}({", ".join(map((lambda x: f'{x[0]}: {x[1]}'), self.def_params))}):\n{"   \n".join(map(repr, self.body))}'


class ModuleNode(ASTNode):
    def __init__(self, body, pos):
        self.body = body
        super().__init__("Module", pos)

    def __repr__(self):
        return "\n".join(map(repr, self.body))
