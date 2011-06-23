# -*- coding: utf-8 -*-

from datetime import datetime
from reportlab.lib.units import mm

_valores = {}
_lista_dias = {}

def add_fecha(id_grupo, fecha):
    if not _lista_dias.has_key(id_grupo):
        _lista_dias[id_grupo] = []
        
    _lista_dias[id_grupo].append(fecha)
    
def existe_fecha(id_grupo, fecha):
    if not _lista_dias.has_key(id_grupo):
        return False
    
    else:
        return fecha in _lista_dias[id_grupo]

def esto_es_una_prueba():
    return '***ESTO ES UNA PRUEBA'

def sum_valor(tipo, valor):
    if not _valores.has_key(tipo):
        _valores[tipo] = 0
        
    _valores[tipo] += valor

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

#def draw_calendars(left, top, w_cell, h_cell, pdf_report, first_day=None,
#                   last_day=None, id_grupo):
#    
#    por_fila = pdf_report.wd / (w_cell * 7)
#    espacio = (pdf_report.wd - w_cell * 7 * por_fila) / (por_fila - 1)
#    
#    day = first_day
#    while day < last_day:
#        
#        day = datetime.fromordinal(day.toordinal() + 1)    
    

def draw_calendar(left, top, w_cell, h_cell, pdf_report, first_day=None, 
                  last_day=None, id_grupo=None):
    
    if first_day is None:
        day1 = datetime(last_day.year, last_day.month, 1)
        first_day = day1
        
    else:
        day1 = datetime(first_day.year, first_day.month, 1)
    
    next_month = datetime.fromordinal(day1.toordinal() + 31)
    last_day_month = datetime.fromordinal(datetime(next_month.year, next_month.month, 1).toordinal() - 1)
    
    if last_day is None:
        last_day = last_day_month
                    
    left = left * mm
    top = top * mm
    w_cell = w_cell * mm
    h_cell = h_cell * mm
    
    dias = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
             'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    pdf_report.canvas.drawString(left + 50, top + 2, '%s %d' % (meses[day1.month-1], day1.year))
    
    # líneas horizontales
    for i in range(7):
        pdf_report.canvas.line(left, top - i * h_cell, left + w_cell * 7, top - i * h_cell)
        pdf_report.canvas.drawString(left + i * w_cell + 8, top - 10, dias[i])
        
    # líneas verticales
    for i in range(8):
        pdf_report.canvas.line(left + i * w_cell, top, left + i * w_cell, top - h_cell * 6)
    
    day = day1
    week = 1
    while day.month == day1.month:
        wd = day.weekday()
        if wd == 0 and day.day > 1:
            week += 1
            
        pdf_report.canvas.saveState()            
        
        if day.day == first_day.day:
            pass
#            pdf_report.canvas.setFillColorRGB(0, 0, 1.0)
            
        elif day.day < first_day.day or day.day > last_day.day:
            pdf_report.canvas.setFillColorRGB(0.5, 0.5, 0.5)
            
        if id_grupo != None:
            if existe_fecha(id_grupo, day.strftime('%d/%m/%Y')):
                pdf_report.canvas.setFillColorRGB(1.0, 0, 0)
            
        pdf_report.canvas.drawString(left + wd * w_cell + 8, top - week * h_cell - 10, str(day.day))
        
        pdf_report.canvas.restoreState()
    
        day = datetime.fromordinal(day.toordinal() + 1)
       
    
    pdf_report.canvas.saveState()
    pdf_report.canvas.setFillColorRGB(0.5, 0.5, 0.5)
    for i in range(day1.weekday()):       
        pdf_report.canvas.rect(left + i * w_cell, top - 2 * h_cell, w_cell, h_cell, fill=1)
        
    for i in range(last_day_month.weekday() + 1, 7):
        pdf_report.canvas.rect(left + i * w_cell, top - (week + 1) * h_cell, w_cell, h_cell, fill=1)
        
    pdf_report.canvas.restoreState()
    
    return ''
         

