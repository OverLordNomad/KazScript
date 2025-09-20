from core.ast import (
    KazAssign,
    KazBinOp,
    KazEcho,
    KazNumber,
    KazProgram,
    KazVariable
)

def print_ast(node, indent=0):
    prefix = '  ' * indent

    match node:
        case KazProgram(statements):
            print(f'{prefix}Бағдарлама (Program)')
            for stmt in statements:
                print_ast(stmt, indent + 1)

        case KazAssign(name, expr):
            print(f'{prefix}Айнымалыны меншіктеу: {name}')
            print_ast(expr, indent + 1)

        case KazEcho(expr):
            print(f'{prefix}Шығару (echo)')
            print_ast(expr, indent + 1)

        case KazBinOp(left, op, right):
            print(f'{prefix}Операция {op}')
            print_ast(left, indent + 1)
            print_ast(right, indent + 1)

        case KazNumber(value):
            print(f'{prefix}Сан: {value}')

        case KazVariable(name):
            print(f'{prefix}Айнымалы: {name}')

        case _:
            print(f'{prefix}Белгісіз түйін: {node}')

