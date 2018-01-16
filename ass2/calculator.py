#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'plus': 'PLUS2',
    'minus': 'MINUS2',
    'times': 'TIMES2',
    'divide': 'DIVIDE2',
    'power': 'EXP2'
}

string_to_int = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
}

tokens = [
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN', 'HUNDRED', 'THOUSAND', 'SNUMBER'
] + list(reserved.values())


t_ignore = " \t\n"

t_PLUS = r'\+'
t_MINUS = r'-'
t_EXP = r'\*\*'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_HUNDRED(t):
    r'hundred'
    return t

def t_THOUSAND(t):
    r'thousand'
    return t

def t_SNUMBER(t):
    r'twelve|seven|ten|seventeen|forty|four|sixty|eighteen|thirteen|sixteen|fifty|twenty|six|two|eleven|hundred|thousand|eighty|fourteen|five|nineteen|one|fifteen|seventy|thirty|ninety|nine|three|eight'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Parsing rules
precedence = (
	('left', 'PLUS', 'MINUS'),
    ('left', 'PLUS2', 'MINUS2'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'TIMES2', 'DIVIDE2'),
        ('left', 'EXP'),
        ('left', 'EXP2'),
        ('left', 'HUNDRED'),
        ('left', 'THOUSAND'),
        ('left', 'SNUMBER'),
        ('right', 'UMINUS'),
)

def p_statement_assign(p):
	'statement : NAME EQUALS expression'
	p[1]=p[3]

def p_statement_expr(p):
        'statement : expression'
        print(p[1])

def p_expression_binop(p):
    """
    expression : expression PLUS expression
              | expression MINUS expression
              | expression TIMES expression
              | expression DIVIDE expression
              | expression EXP expression
              | expression PLUS2 expression
              | expression MINUS2 expression
              | expression TIMES2 expression
              | expression DIVIDE2 expression
              | expression EXP2 expression
    """
    print('plus', [repr(p[i]) for i in range(0,4)])
    if p[2] == '+' or p[2] == 'plus':
        p[0] = p[1] + p[3]
    elif p[2] == '-' or p[2] == 'minus':
        p[0] = p[1] - p[3]
    elif p[2] == '*' or p[2] == 'times':
        p[0] = p[1] * p[3]
    elif p[2] == '/' or p[2] == 'divide':
        p[0] = p[1] / p[3]
    elif p[2] == '**' or p[2] == 'power':
        p[0] = p[1] ** p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        p[0] = p[1]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_snumber(p):
    '''
    expression : SNUMBER
    '''
    print("snum", [repr(p[i]) for i in range(0,2)])
    p[0] = string_to_int[p[1]]

def p_expression_snumber(p):
    '''
    expression : expression SNUMBER
    '''
    print("exp snum", [repr(p[i]) for i in range(0,3)])
    p[0] = p[1] + string_to_int[p[2]]

def p_snumber_hundred(p):
    '''
    expression : SNUMBER HUNDRED
    '''
    print('hundred', [repr(p[i]) for i in range(0,3)])
    p[0] = string_to_int[p[1]]*100

def p_expression_hundred(p):
    '''
    expression : expression SNUMBER HUNDRED
    '''
    print('exp hundred', [repr(p[i]) for i in range(0,4)])
    p[0] = p[1] + string_to_int[p[2]]*100

def p_expression_thousand(p):
    '''
    expression : expression THOUSAND
    '''
    print('thousand', [repr(p[i]) for i in range(0,3)])
    p[0] = p[1]*1000

def p_error(p):
    if p:
        print("syntax error at {0}".format(p.value), p.type)
    else:
        print("syntax error at EOF")

def process(data):
	lex.lex()
	yacc.yacc()
	yacc.parse(data)

if __name__ == "__main__":
	print("Enter the Equation")
	data = sys.stdin.readline()
	process(data)
