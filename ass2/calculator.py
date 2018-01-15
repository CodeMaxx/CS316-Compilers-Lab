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

tokens = [
        'NAME', 'NUMBER',
        'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
        'LPAREN', 'RPAREN',
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
        # print([repr(p[i]) for i in range(0,4)])
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

def p_error(p):
	if p:
		print("syntax error at {0}".format(p.value))
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
