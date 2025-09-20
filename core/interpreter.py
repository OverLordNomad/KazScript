"""Interpreter for KazScript programming language."""

class Interpreter:
    def __init__(self):
        self.env = {}  # айнымалыларды сақтау

    def eval(self, node):
        # Әрбір AST-нодың ішінде өзінің _eval функциясы бар
        if hasattr(node, '_eval') and callable(node._eval):
            return node._eval(self, node)
        else:
            raise TypeError(f"Белгісіз ноуд түрі: {type(node).__name__}")
