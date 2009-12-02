# -*- coding: utf-8 -*-

prueba = __import__('prueba', globals(), locals())

script = '{{prueba.sum_valor(#TIPO#, #HORAS#)}}'

# procesar cadena de script
if '{{' in script and '}}' in script:
    script = script[(script.find('{{') + 2):script.find('}}')]
    script = script.replace('#TIPO#', '1')
    script = script.replace('#HORAS#', '30')
    print script
    eval(script)

print eval('prueba.get_valor(1)')
print eval('prueba.get_date("%B %a, %y")')
