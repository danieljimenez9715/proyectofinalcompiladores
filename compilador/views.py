from django.shortcuts import render
from .analizadores.lexer import *
from .analizadores.parser import *
import copy

def Compilador(request):
    return render(request, 'compilador.html')

def Validar(request):
    codigo = request.POST['codigo'] 
    respuesta = compilar(codigo)
    respuesta['codigo'] = codigo

    return render(request, 'compilador.html', respuesta)

def compilar(codigo):
    global errores_lexer
    errores_lexer.clear()
    plylex_results = []

    resultado_analisis = ejecutar_codigo(codigo)
    
    analizador_lexico.lineno = 1
    analizador_lexico.input(codigo)

    while True:
        tkn = analizador_lexico.token()
        if not tkn : break
        plylex_results.append(copy.copy(str(tkn)))

    resultado_analisis = "\n".join(resultado_analisis)
    plylex_results = "\n".join(plylex_results)

    return { 'resultado_analisis':resultado_analisis, 'resultado_lexico':plylex_results }
