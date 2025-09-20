"""Lexical analyzer for KazScript programming language"""

import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

# Тек екі кілт сөз
KEYWORDS = {
    'айнымалы': 'АЙНЫМАЛЫ',
    'шығару': 'ШЫҒАРУ',
}

TOKEN_SPECIFICATION = [
    ('NUMBER',  r'\d+(\.\d*)?'),  # сандар
    ('ID',      r'[a-zA-Zа-яА-ЯәғқңөұүһӘҒҚҢӨҰҮҺ_][a-zA-Zа-яА-ЯәғқңөұүһӘҒҚҢӨҰҮҺ_0-9]*'),  # айнымалы аттары
    ('OP',      r'[:]=|==|!=|<=|>=|[+\-*/=<>]'),  # операциялар (=, +, - ...)
    ('SKIP',    r'[ \t]+'),       # пробелдер мен табуляция
    ('NEWLINE', r'\n'),           # жаңа жол
    ('LPAREN',  r'\('),           # ашық жақша
    ('RPAREN',  r'\)'),           # жабық жақша
    ('MISMATCH',r'.'),            # қате символ
]


def lex(code):
    # Бір regex қылып жинау
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()

        match kind:
            case 'NUMBER':
                yield Token('NUMBER', float(value) if '.' in value else int(value))

            case 'ID':
                if value in KEYWORDS:
                    yield Token(KEYWORDS[value], value)
                else:
                    yield Token('ID', value)

            case 'NEWLINE' | 'SKIP':
                continue

            case 'LPAREN' | 'RPAREN' | 'OP':
                yield Token(kind, value)

            case 'MISMATCH':
                raise SyntaxError(f'Күтпеген символ: {value!r}')
