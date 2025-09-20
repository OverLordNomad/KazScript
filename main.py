from core.lexer import lex
from core.parser import Parser
from core.interpreter import Interpreter

if __name__ == '__main__':
    code = open('test.kzy', 'r', encoding='utf-8').read()

    tokens = lex(code)          # Лексер
    parser = Parser(tokens)
    ast = parser.parse()        # AST құру

    interpreter = Interpreter()
    interpreter.eval(ast)       # Тікелей орындау
