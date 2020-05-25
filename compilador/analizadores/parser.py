from .ply import yacc as yacc
import os
import codecs

from .lexer import tokens, errores_lexer

errores_parser = []
variables = {}

precedence = (
    ('right', 'ASIGNAR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    # ('right', 'UMINUS'),
)

def p_declaracion_asignar(t):
    '''
    declaracion : IDENTIFICADOR ASIGNAR expresion 
                | IDENTIFICADOR ASIGNAR CADENA 
    '''
    variables[t[1]] = t[3]

def p_declaracion_expr(t):
    'declaracion : expresion'
    # print("Resultado: " + str(t[1]))
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion
                |   expresion RESTA expresion
                |   expresion MULTIPLICACION expresion
                |   expresion DIVISION expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '**':
        i = t[3]
        t[0] = t[1]
        while i > 1:
            t[0] *= t[1]
            i -= 1

# def p_expresion_uminus(t):
#     'expresion : RESTA expresion %prec UMINUS'
#     t[0] = -t[2]

def p_expresion_grupo(t):
    '''
    expresion  : PARENTESIS_IZQ expresion PARENTESIS_DER
                | LLAVE_IZQ expresion LLAVE_DER
                | CORCHETE_IZQ expresion CORCHETE_DER
    '''
    t[0] = t[2]

def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENOR_QUE expresion 
                |  expresion MAYOR_QUE expresion 
                |  expresion MENOR_IGUAL expresion 
                |  expresion MAYOR_IGUAL expresion 
                |  expresion IGUAL expresion 
                |  expresion DISTINTO expresion
                |  PARENTESIS_IZQ expresion PARENTESIS_DER MENOR_QUE PARENTESIS_IZQ expresion PARENTESIS_DER
                |  PARENTESIS_IZQ expresion PARENTESIS_DER MAYOR_QUE PARENTESIS_IZQ expresion PARENTESIS_DER
                |  PARENTESIS_IZQ expresion PARENTESIS_DER MENOR_IGUAL PARENTESIS_IZQ expresion PARENTESIS_DER 
                |  PARENTESIS_IZQ  expresion PARENTESIS_DER MAYOR_IGUAL PARENTESIS_IZQ expresion PARENTESIS_DER
                |  PARENTESIS_IZQ  expresion PARENTESIS_DER IGUAL PARENTESIS_IZQ expresion PARENTESIS_DER
                |  PARENTESIS_IZQ  expresion PARENTESIS_DER DISTINTO PARENTESIS_IZQ expresion PARENTESIS_DER
    '''
    if t[2] == "<": t[0] = t[1] < t[3]
    elif t[2] == ">": t[0] = t[1] > t[3]
    elif t[2] == "<=": t[0] = t[1] <= t[3]
    elif t[2] == ">=": t[0] = t[1] >= t[3]
    elif t[2] == "==": t[0] = t[1] is t[3]
    elif t[2] == "!=": t[0] = t[1] != t[3]
    elif t[3] == "<":
        t[0] = t[2] < t[4]
    elif t[2] == ">":
        t[0] = t[2] > t[4]
    elif t[3] == "<=":
        t[0] = t[2] <= t[4]
    elif t[3] == ">=":
        t[0] = t[2] >= t[4]
    elif t[3] == "==":
        t[0] = t[2] is t[4]
    elif t[3] == "!=":
        t[0] = t[2] != t[4]


def p_expresion_booleana(t):
    '''
    expresion   :  expresion AND expresion 
                |  expresion OR expresion 
                |  expresion NOT expresion 
                |  PARENTESIS_IZQ expresion AND expresion PARENTESIS_DER
                |  PARENTESIS_IZQ expresion OR expresion PARENTESIS_DER
                |  PARENTESIS_IZQ expresion NOT expresion PARENTESIS_DER
    '''
    if t[2] == "&&":
        t[0] = t[1] and t[3]
    elif t[2] == "||":
        t[0] = t[1] or t[3]
    elif t[2] == "!":
        t[0] =  t[1] is not t[3]
    elif t[3] == "&&":
        t[0] = t[2] and t[4]
    elif t[3] == "||":
        t[0] = t[2] or t[4]
    elif t[3] == "!":
        t[0] =  t[2] is not t[4]

def p_expresion_condicional_si(t):
    '''
    expresion :  SI LLAVE_IZQ expresion LLAVE_DER CORCHETE_IZQ  expresion CORCHETE_DER
    '''
    if t[2]: 
        t[0] = t[4]
    
def p_expresion_condicional_sino(t):
    '''
    expresion : expresion SINO CORCHETE_IZQ expresion CORCHETE_DER
    '''
    if t[1] == None:
        t[0] = t[4]
    else:
        t[0] = t[1]

def p_expresion_ciclo_for(t):
    '''
    expresion : PARA LLAVE_IZQ declaracion COMA expresion COMA declaracion LLAVE_DER CORCHETE_IZQ expresion CORCHETE_DER
            |    PARA LLAVE_IZQ declaracion COMA expresion COMA declaracion LLAVE_DER CORCHETE_IZQ declaracion CORCHETE_DER
    '''
    t[0] = 0

def p_expresion_ciclo_while(t):
    '''
    expresion : MIENTRAS LLAVE_IZQ expresion LLAVE_DER CORCHETE_IZQ expresion CORCHETE_DER
            |   MIENTRAS LLAVE_IZQ expresion LLAVE_DER CORCHETE_IZQ declaracion CORCHETE_DER
    '''
    t[0] = 0

def p_expresion_do_while(t):
    '''
    expresion : HACER CORCHETE_IZQ expresion CORCHETE_DER MIENTRAS LLAVE_IZQ expresion LLAVE_DER 
            |   HACER CORCHETE_IZQ declaracion CORCHETE_DER MIENTRAS LLAVE_IZQ expresion LLAVE_DER
    '''
    t[0] = 0

def p_expresion_numero(t):
    'expresion : ENTERO'
    t[0] = t[1]

def p_expresion_cadena(t):
    'expresion : COMILLAS_DOBLES expresion COMILLAS_DOBLES'
    t[0] = t[2]

def p_expresion_nombre(t):
    'expresion : IDENTIFICADOR'
    try:
        t[0] = variables[t[1]]
    except LookupError:
        guardar_error("Identificador indefinido", str(linea_leida), t[1])
        t[0] = 0

def p_expresion_imprimir(t):
    '''
    expresion : IMPRIMIR LLAVE_IZQ IDENTIFICADOR LLAVE_DER
            |   IMPRIMIR LLAVE_IZQ CADENA LLAVE_DER
    '''
    if t[3][0] != '"':
        try:
            t[0] = variables[t[3]]
        except LookupError:
            guardar_error("Identificador indefinido", str(linea_leida), t[3])
            t[0] = 0
    else:
        t[0] = t[3]

def p_error(t):
    global errores_parser
    if t:
        mensaje = "Linea {} Columna {}. tipo:{} -> \"{}\"".format(str(linea_leida), str(t.lexpos), str(t.type), str(t.value))
    else:
        mensaje = "Linea {}. Error {} (desconocido)".format(str(linea_leida), t)
    errores_parser.append(mensaje)

def guardar_error(mensaje_error, linea, valor):
    global errores_parser
    mensaje = "Linea {}. {} -> {}".format(linea, mensaje_error, valor)
    errores_parser.append(mensaje)


parser = yacc.yacc()

def ejecutar_codigo(codigo):
    global errores_parser
    errores_parser.clear()

    global linea_leida
    linea_leida = 0

    salida_parser = []

    for lineaDeCodigo in codigo.splitlines():
        linea_leida = linea_leida + 1
        if lineaDeCodigo:
            resultado = parser.parse(lineaDeCodigo)
            if resultado:
                salida = "Linea {} -> {}".format(str(linea_leida), str(resultado))
                salida_parser.append(salida)

    return errores_parser

