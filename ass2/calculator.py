#!/usr/bin/python3

import sys
import ply.lex as lex
import ply.yacc as yacc

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
        'LPAREN', 'RPAREN', 'HUNDRED', 'THOUSAND', 'SNUMBER', 'TENS', 'BIGTENS'
]

t_ignore = " \t\n"

t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_PLUS(t):
    r'\+|\bplus\b'
    t.value = '+'
    return t

def t_MINUS(t):
    r'\-|\bminus\b'
    t.value = '-'
    return t

def t_EXP(t):
    r'\*\*|\bpower\b'
    t.value = '**'
    return t

def t_TIMES(t):
    r'\*|\btimes\b'
    t.value = '*'
    return t

def t_DIVIDE(t):
    r'\/|\bdivide\b'
    t.value = '/'
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_HUNDRED(t):
    r'\bhundred'
    return t

def t_THOUSAND(t):
    r'\bthousand'
    return t

def t_BIGTENS(t):
    r'\bninety\b|\beighty\b|\bseventy\b|\bsixty\b|\bfifty\b|\bforty\b|\bthirty\b|\btwenty\b'
    return t

def t_TENS(t):
    r'\bnineteen\b|\beighteen\b|\bseventeen\b|\bsixteen\b|\bfifteen\b|\bfourteen\b|\bthirteen\b|\btwelve\b|\beleven\b|\bten\b'
    return t

def t_SNUMBER(t):
    r'\bnine\b|\beight\b|\bseven\b|\bsix\b|\bfive\b|\bfour\b|\bthree\b|\btwo\b|\bone\b'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Parsing rules
# TODO - Check for correctness
precedence = (
	('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXP'),
    ('right', 'UMINUS'),
    ('left', 'HUNDRED'),
    ('left', 'THOUSAND'),
    ('left', 'SNUMBER'),
    ('left', 'TENS'),
    ('left', 'BIGTENS'),
)

def p_statement_assign(p):
	'''
    statement : NAME EQUALS expression
                | NAME EQUALS sexpr
    '''
	p[1]=p[3]

def p_statement_expr(p):
    '''
    statement : expression
                | sexpr
    '''
    print(p[1])

def p_expression_binop(p):
    """
    expression : expression PLUS expression
              | expression MINUS expression
              | expression TIMES expression
              | expression DIVIDE expression
              | expression EXP expression
              | sexpr PLUS sexpr
              | sexpr MINUS sexpr
              | sexpr TIMES sexpr
              | sexpr DIVIDE sexpr
              | sexpr EXP sexpr
              | expression PLUS sexpr
              | expression MINUS sexpr
              | expression TIMES sexpr
              | expression DIVIDE sexpr
              | expression EXP sexpr
              | sexpr PLUS expression
              | sexpr MINUS expression
              | sexpr TIMES expression
              | sexpr DIVIDE expression
              | sexpr EXP expression
    """
    # print('plus', [repr(p[i]) for i in range(0,4)])

    try:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]
    except:
        pass

def p_expression_uminus(p):
    '''
    expression : MINUS expression %prec UMINUS
                | MINUS sexpr %prec UMINUS
    '''
    p[0] = -p[2]

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
                | LPAREN sexpr RPAREN
    '''
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

def p_snumber_tens_bigtens(p):
    '''
    sexpr : SNUMBER
            | TENS
            | BIGTENS
    '''
    # print("snum", [repr(p[i]) for i in range(0,2)])
    p[0] = string_to_int[p[1]]

def p_bigtens_snumber(p):
    '''
    sexpr : BIGTENS SNUMBER
    '''
    # print("exp snum", [repr(p[i]) for i in range(0,3)])
    p[0] = string_to_int[p[1]] + string_to_int[p[2]]

def p_snumber_hundred(p):
    '''
    sexpr : SNUMBER HUNDRED
    '''
    # print('hundred', [repr(p[i]) for i in range(0,3)])
    p[0] = string_to_int[p[1]]*100

def p_snumber_hundred_expr(p):
    '''
    sexpr : SNUMBER HUNDRED sexpr
    '''
    # print('hundred', [repr(p[i]) for i in range(0,3)])
    if not isinstance(p[3], int) or (p[3] > 99 or p[3] < -99):
        print('syntax error at HUNDRED')
    p[0] = string_to_int[p[1]]*100 + p[3]

def p_expression_thousand(p):
    '''
    sexpr : sexpr THOUSAND
    '''
    # print('thousand', [repr(p[i]) for i in range(0,3)])
    if not isinstance(p[1], int) or (p[1] > 99 or p[1] < -99):
        print('syntax error at THOUSAND')
    else:
        p[0] = p[1]*1000

def p_expression_thousand_expr(p):
    '''
    sexpr : sexpr THOUSAND sexpr
    '''
    # print('thousand', [repr(p[i]) for i in range(0,3)])
    if not isinstance(p[1], int) or (p[1] > 99 or p[1] < -99):
        print('syntax error at THOUSAND')
    else:
        p[0] = p[1]*1000 + p[3]

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
