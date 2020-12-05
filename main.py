import ply.lex as lex
import ply.yacc as yacc




def modulo(val):
    mod = val % 1234577
    if mod < 0:
        mod += 1234577

    return mod


def divide(a, b):
    p = 1234577
    m = 0

    while (a + m*p) % b != 0:
        m += 1

    return modulo(int((a + m*p) / b))


tokens = (
    'NAME', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'MINUSPOWER', 'EQUALS',
    'LPAREN', 'RPAREN',
)

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POWER = r'\^'
t_MINUSPOWER = r'\^\ *-'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
        print(str(t.value) + " ", end="")
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'
t_ignore_NEWLINE = r'\\n'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),
)

names = {}
lexer = lex.lex()


def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]


def p_statement_expr(t):
    'statement : expression'
    global COW
    print("\n" + str(t[1]))


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER NUMBER'''

    if t[2] == '+':
        print('+ ', end="")
        t[0] = modulo(t[1] + t[3])

    elif t[2] == '-':
        print('- ', end="")
        t[0] = modulo(t[1] - t[3])

    elif t[2] == '*':
        print('* ', end="")
        t[0] = modulo(t[1] * t[3])

    elif t[2] == '/':
        print('/ ', end="")
        t[0] = divide(t[1], t[3])

    elif t[2] == '^':
        print('^ ', end="")
        t[0] = modulo(modulo(t[1]) ** modulo(t[3]))


def p_expression_minuspower(t):
    'expression : expression MINUSPOWER NUMBER'
    print('^- ', end="")
    t[0] = modulo(divide(1, t[1]) ** t[3])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = modulo(-t[2])


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = modulo(t[2])


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = modulo(t[1])


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()


while True:
    try:
        s = input('calc > ')
    except EOFError:
        break

    try:
        parser.parse(s)
    except AttributeError:
        pass
