# -*- coding: utf-8 -*-

from reports import Report
#from reportPdf import ReportPdf
from reportPlainText import ReportPlainText
from unidadescompartidas import conexion
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
from libpy.implementation.enviaremail import enviar_email

#f = file('./report1.xml', 'r')
#f = file('D:/workspace/tandemdev/tandem/informes/resumen_mensual.xml', 'r')
f = file('./mail_resumen_mensual.xml', 'r')
try:    
    informe = Report(xml=f.read())
    
#    print informe.xml
    
    conector = conexion()
#    pdf = ReportPdf(informe, conector)    
#    pdf.writeReport(pdf_file='./hello.pdf', params=[('NUMERO_ALUMNOS', '100', 'int')])

    txt = ReportPlainText(informe, conector)
    resultado = txt.writeReport(params=[('P_MES', 'Noviembre', 'str'),
                                        ('P_MONTH', 'November', 'str'),
                                        ('P_FECHA_LIMITE', '2 de Dicimebre', 'str'),
                                        ('P_DEADLINE', 'December 2', 'str'),
                                        ('P_HOY', '23 de Noviembre', 'str'),
                                        ('P_TODAY', 'November 23', 'str'),
                                        ('P_PROFESOR', '1', 'int'),
                                        ('P_FECHA_INICIO', '01/11/2009', 'date'),
                                        ('P_FECHA_FIN', '23/11/2009', 'date')], debug=False)
    #print resultado
    
    print enviar_email('tengounplanb@gmail.com', ['leon.domingo@ender.es'],
                       'Resumen mensual', resultado,
                       'smtp.gmail.com', 'tengounplanb@gmail.com', 'nitelite01')
finally:
    f.close()