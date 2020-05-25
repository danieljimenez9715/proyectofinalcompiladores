from .ply import lex as lex
import os
import codecs

errores_lexer = []

tokens =  (
    'IDENTIFICADOR',
    'ENTERO',
    'CADENA',
    'ASIGNAR',
    'IMPRIMIR',

    'SUMA', 'RESTA',
    'MULTIPLICACION', 'DIVISION',
    'POTENCIA', 'MODULO',

    'SI', 'SINO',
    'HACER', 'MIENTRAS', 'PARA',
    
    'AND', 'OR', 'NOT',
    'MENOR_QUE',  'MAYOR_QUE',
    'MENOR_IGUAL', 'MAYOR_IGUAL',
    'IGUAL', 'DISTINTO',
    
    'PARENTESIS_IZQ', 'PARENTESIS_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER',
    'LLAVE_IZQ', 'LLAVE_DER',
    
    'NUMERAL', 'PUNTO_COMA', 'COMA',
    'COMILLAS_DOBLES',
)

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'

t_ASIGNAR = r'<<'

t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENOR_QUE = r'<'
t_MAYOR_QUE = r'>'
t_PUNTO_COMA = ';'
t_COMA = r','
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_LLAVE_IZQ = r'{'
t_LLAVE_DER = r'}'
t_COMILLAS_DOBLES = r'\"'

def t_IMPRIMIR(t):
    r'@mostrar'
    return t

def t_SINO(t):
    r'sino\?'
    return t

def t_SI(t):
    r'si\?'
    return t

def t_HACER(t):
    r'@hacer'
    return t

def t_MIENTRAS(t):
    r'@mientras'
    return t

def t_PARA(t):
    r'@para'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'\w+(_\d\w)*'
    return t

def t_CADENA(t):
   r'\"(\w+ \ *\w*\d* \ *)\"'
   return t

def t_NUMERAL(t):
    r'\#'
    return t

def t_MENOR_IGUAL(t):
    r'<='
    return t

def t_MAYOR_IGUAL(t):
    r'>='
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_DISTINTO(t):
    r'!='
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")

def t_comments_ONELine(t):
    r'\/\/(.)*\n'
    t.lexer.lineno += 1
    print("Comentario de una linea")

t_ignore =' \t'

def t_error( t):
    global errores_lexer
    estado = "Error Lexico. Linea {} Pos {}. (Token invalido) Valor {} ".format(str(t.lineno), str(t.lexpos), str(t.value))
    errores_lexer.append(estado)
    t.lexer.skip(1)

analizador_lexico = lex.lex()
