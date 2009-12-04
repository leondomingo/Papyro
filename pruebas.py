# -*- coding: utf-8 -*-

from unidadescompartidas import conexion
from reports import Report
#from reportPdf import ReportPdf
from reportPlainText import ReportPlainText
import os.path
#from libpy.implementation.enviaremail import enviar_email

conector = conexion()

#report_path = os.path.join(conector.datosconexion.getVariable('ruta_informes'), 
#                           'MailResumenMensual/ResumenMensualEnglish.xml')

#report_path = os.path.join(conector.datosconexion.getVariable('ruta_informes'), 
#                           'MailResumenMensual/MailResumenMensual.xml')

report_path = os.path.join(conector.datosconexion.getVariable('ruta_informes'),
                           'MailResumenMensual_ultimo-dia/MailResumenMensual_ultimo-dia.xml')

#informe = Report(reportfile=report_path)
informe = Report(reportfile='./report1.xml')

#f = file('./report1.xml', 'r')
#f = file(report_path, 'r')
#f = file('./report1.xml', 'r')
#try:

#    print informe.xml

#pdf = ReportPdf(informe, conector)
#pdf.writeReport(pdf_file='./report1.pdf', params=[('P_NUMERO_GRUPOS', '30', 'int'),
#                                                  ('P_GRUPO', '390', 'int')], debug=False)

txt = ReportPlainText(informe, conector)
resultado = txt.writeReport(text_file='./report1.txt',
                            params=[('P_NUMERO_GRUPOS', '30', 'int'),
                                    ('P_GRUPO', '390', 'int')])

#print resultado

#txt = ReportPlainText(informe, conector)
#resultado = txt.writeReport(report_path=report_path,
#                            params=[('P_MES', 'Noviembre', 'str'),
#                                    ('P_MONTH', 'November', 'str'),
#                                    ('P_MANANA', '1 de Diciembre', 'str'),
#                                    ('P_TOMORROW', 'December 1', 'str'),
#                                    ('P_DEADLINE', 'December 2', 'str'),
#                                    ('P_HOY', '30 de Noviembre', 'str'),
#                                    ('P_TODAY', 'November 30', 'str'),
#                                    ('P_PROFESOR', '1', 'int'),
#                                    ('P_FECHA_INICIO', '01/11/2009', 'date'),
#                                    ('P_FECHA_FIN', '30/11/2009', 'date')], debug=False)
#
#print resultado

#print enviar_email(('atenea@tandem-madrid.com', 'Atenea - Tandem Madrid'),
#                   [('leon.domingo@ender.es', 'León Domingo Ortín')],
#                   'Resumen mensual', resultado,
#                   'smtp.dipro.es', 'atenea@tandem-madrid.com', 'A1s2d3f4')

print 'The end'
#finally:
#    f.close()