# -*- coding: utf-8 -*-

from reports import Report
from reportPdf import ReportPdf
from unidadescompartidas import conexion
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4

f = file('./report0.xml', 'r')
try:    
    informe = Report(xml=f.read())
    
    print informe.xml
    
    conector = conexion()
    #informe.write(conector)
    pdf = ReportPdf(informe, conector)
    pdf.writeReport(pdf_file='./hello.pdf', params=[('NUMERO_ALUMNOS', '100', 'int')])
finally:
    f.close()