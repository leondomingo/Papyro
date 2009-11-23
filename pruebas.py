# -*- coding: utf-8 -*-

from reports import Report
#from reportPdf import ReportPdf
from reportPlainText import ReportPlainText
from unidadescompartidas import conexion
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
from libpy.implementation.enviaremail import enviar_email
import os.path

#f = file('./report1.xml', 'r')
#f = file('D:/workspace/tandemdev/tandem/informes/resumen_mensual.xml', 'r')
conector = conexion()

#report_path = os.path.join(conector.datosconexion.getVariable('ruta_informes'), 
#                           'MailResumenMensual/MailResumenMensual.xml')

report_path = os.path.join(conector.datosconexion.getVariable('ruta_informes'), 
                           'MailResumenMensual/MailResumenMensual.xml')

f = file(report_path, 'r')
try:    
    informe = Report(xml=f.read())    
#    print informe.xml
    
#    pdf = ReportPdf(informe, conector)    
#    pdf.writeReport(pdf_file='./hello.pdf', params=[('NUMERO_ALUMNOS', '100', 'int')])

    txt = ReportPlainText(informe, conector)
    resultado = txt.writeReport(report_path=report_path,
                                params=[('P_MES', 'Noviembre', 'str'),
                                        ('P_MONTH', 'November', 'str'),
                                        ('P_FECHA_LIMITE', '2 de Dicimebre', 'str'),
                                        ('P_DEADLINE', 'December 2', 'str'),
                                        ('P_HOY', '23 de Noviembre', 'str'),
                                        ('P_TODAY', 'November 23', 'str'),
                                        ('P_PROFESOR', '1', 'int'),
                                        ('P_FECHA_INICIO', '01/11/2009', 'date'),
                                        ('P_FECHA_FIN', '23/11/2009', 'date')], debug=False)
    print resultado

    print enviar_email(('atenea@tandem-madrid.com', 'Atenea - Tandem Madrid'),
                       [('leon.domingo@ender.es', 'León Domingo Ortín'), 
                        ('dgsalas@ender.es', 'Domingo G. Salas')],
                       'Resumen mensual 2', resultado,
                       'smtp.dipro.es', 'atenea@tandem-madrid.com', 'A1s2d3f4',
                       nombre_remitente='Atenea - Tandem Madrid <atenea@tandem-madrid.com>',
                       nombres_destinatarios=['León Domingo Ortín <leon.domingo@ender.es>',
                                              'Domingo G. Salas <dgsalas@ender.es>'])
    
    print enviar_email('atenea@tandem-madrid.com', ['leon.domingo@ender.es', 'dgsalas@ender.es'],
                       'Resumen mensual 2', resultado,
                       'smtp.dipro.es', 'atenea@tandem-madrid.com', 'A1s2d3f4',
                       nombre_remitente='Atenea - Tandem Madrid <atenea@tandem-madrid.com>',
                       nombres_destinatarios=['León Domingo Ortín <leon.domingo@ender.es>',
                                              'Domingo G. Salas <dgsalas@ender.es>'])
    
finally:
    f.close()