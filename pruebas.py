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
    pdf.writeReport('./hello.pdf')
finally:
    f.close()

#c = canvas.Canvas('./hello.pdf', pagesize=A4)
#
#for f in c.getAvailableFonts():
#    print f
#
#c.saveState()
#c.setFont('Helvetica-Bold', size=12)
#c.translate(200, 200)
##c.scale(1.0, 2.0)
#
## 1
#c.drawString(10, 10, '(1) Estoy en 10, 10')
#
#c.restoreState()
#
#c.saveState()
#c.setFont('Times-Roman', size=20)
#c.translate(100, 100)
#
## 2
#c.drawString(10, 10, '(2) Estoy en 10, 10')
#
#c.restoreState()
#
## 3
#c.drawString(10, 10, '(3) Vuelvo al principio... (10, 10)')
#
#c.showPage()
#c.save()