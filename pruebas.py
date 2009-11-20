# -*- coding: utf-8 -*-

from reports import Report
#from reportPdf import ReportPdf
from reportPlainText import ReportPlainText
from unidadescompartidas import conexion
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4

#f = file('./report1.xml', 'r')
f = file('D:/workspace/tandemdev/tandem/informes/resumen_mensual.xml', 'r')
try:    
    informe = Report(xml=f.read())
    
#    print informe.xml
    
    conector = conexion()
#    pdf = ReportPdf(informe, conector)    
#    pdf.writeReport(pdf_file='./hello.pdf', params=[('NUMERO_ALUMNOS', '100', 'int')])

    txt = ReportPlainText(informe, conector)
    resultado = txt.writeReport(params=[('PROFESOR', '1', 'int')], debug=False)
    print len(resultado)
    print resultado
finally:
    f.close()