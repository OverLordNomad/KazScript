"""Parser for KazScript programming language"""

from core.ast import (
    KazAssign,
    KazBinOp,
    KazEcho,
    KazNumber,
    KazProgram,
    KazVariable
)

class Parser:

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        tok = self.peek()
        if tok and tok.type == token_type:
            self.advance()
            return tok
        raise SyntaxError(f'Күтпеген токен: {tok.type}, күткенім: {token_type}')

    def parse(self):
        statements = []
        while self.peek():
            statements.append(self.statement())
        return KazProgram(statements)

    def statement(self):
        tok = self.peek()
        if not tok:
            return None

        # айнымалы x = 10
        if tok.type == 'АЙНЫМАЛЫ':
            self.advance()  # "айнымалы"
            name = self.expect('ID').value
            op = self.expect('OP')
            if op.value != '=':
                raise SyntaxError("Айнымалы тек '=' арқылы меншіктеледі")
            expr = self.expr()
            return KazAssign(name, expr)

        # шығару x + 2
        elif tok.type == 'ШЫҒАРУ':
            self.advance()
            expr = self.expr()
            return KazEcho(expr)

        # жай ғана өрнек (мысалы x + 5)
        else:
            return self.expr()

    def expr(self):
        return self._term_tail(self.term())

    def _term_tail(self, left):
        tok = self.peek()
        if tok and tok.type == 'OP' and tok.value in ('+', '-'):
            self.advance()
            right = self.term()
            return self._term_tail(KazBinOp(left, tok.value, right))
        return left

    def term(self):
        return self._factor_tail(self.factor())

    def _factor_tail(self, left):
        tok = self.peek()
        if tok and tok.type == 'OP' and tok.value in ('*', '/'):
            self.advance()
            right = self.factor()
            return self._factor_tail(KazBinOp(left, tok.value, right))
        return left

    def factor(self):
        tok = self.peek()
        if tok.type == 'NUMBER':
            self.advance()
            return KazNumber(tok.value)
        elif tok.type == 'ID':
            self.advance()
            return KazVariable(tok.value)
        elif tok.type == 'LPAREN':
            self.advance()
            expr = self.expr()
            self.expect('RPAREN')
            return expr

        raise SyntaxError(f'Күтпеген токен: {tok}')
