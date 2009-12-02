# -*- coding: utf-8 -*-

from datetime import datetime

_valores = {}

def esto_es_una_prueba():
    return '***ESTO ES UNA PRUEBA'

def sum_valor(tipo, horas):
    if not _valores.has_key(tipo):
        _valores[tipo] = 0
        
    _valores[tipo] += horas

def set_valor(tipo, valor):
    _valores[tipo] = valor

def get_valor(tipo):
    if _valores.has_key(tipo):
        return _valores[tipo]
    else:
        return 0

def reset():
    for k in _valores.iterkeys():
        _valores[k] = 0

def get_date(formato):
    return datetime.today().strftime(formato)    
