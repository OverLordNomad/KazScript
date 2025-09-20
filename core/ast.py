"""Abstract Syntax Tree classes for KazScript programming language"""

class KazBase:
    def __init__(self, _eval: callable):
        self._eval = _eval


class KazNumber(KazBase):
    __match_args__ = ("value",)

    def __init__(self, value):
        super().__init__(
            _eval=lambda x, node: node.value
        )
        self.value = value


class KazVariable(KazBase):
    __match_args__ = ("name",)

    def __init__(self, name):
        def _eval(x, node):
            if node.name in x.env:
                return x.env[node.name]
            raise NameError(f"Айнымалы '{node.name}' табылмады")

        super().__init__(_eval)
        self.name = name


class KazBinOp(KazBase):
    __match_args__ = ("left", "op", "right")

    def __init__(self, left, op, right):
        def _eval(x, node):
            _left = x.eval(node.left)
            _right = x.eval(node.right)

            operators = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
            }

            if node.op in operators:
                return operators[node.op](_left, _right)
            else:
                raise ValueError(f"Белгісіз оператор: {node.op}")

        super().__init__(_eval)
        self.left = left
        self.op = op
        self.right = right


class KazAssign(KazBase):
    __match_args__ = ("name", "expr")

    def __init__(self, name, expr):
        super().__init__(
            _eval=lambda x, node: x.env.update({node.name: x.eval(node.expr)}) or None
        )
        self.name = name
        self.expr = expr


class KazEcho(KazBase):
    __match_args__ = ("expr",)

    def __init__(self, expr):
        super().__init__(
            _eval=lambda x, node: print(x.eval(node.expr))
        )
        self.expr = expr


class KazProgram(KazBase):
    __match_args__ = ("statements",)

    def __init__(self, statements):
        super().__init__(
            _eval=lambda x, node: [x.eval(stmt) for stmt in node.statements]
        )
        self.statements = statements
