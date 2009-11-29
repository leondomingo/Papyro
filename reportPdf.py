# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reports
#from random import seed, randint

class ReportPdf(object):
    
    def __init__(self, report, conector):
        self.report = report
        self.conector = conector
        self.canvas = None
        self.hg = 0
        self.wd = 0
        self.cur_page = None
        self.debug = False
        
    def newPage(self):
        
        if self.debug: print '***NEW PAGE*****************'
        
        # margin
        m_left = self.report.margin_left * mm
        m_right = self.report.margin_right * mm
        m_top = self.report.margin_top * mm
        m_bottom = self.report.margin_bottom * mm
        
        # anchura de A4
        wd0 = 210 * mm
        hg0 = 297 * mm
        
        # page_header
        ph_height = 0
        if self.cur_page.page_header != None:
            ph_height = self.cur_page.page_header.height * mm
            
        # page_footer
        pf_height = 0
        
        # anchura con márgenes
        self.wd = wd0 - m_left - m_right
        self.hg = hg0 - m_top - m_bottom - ph_height - pf_height
        
        # mover origen
        self.canvas.translate(m_left, self.hg + m_bottom + pf_height)
        
        # dibujar espacio con los márgenes
#        self.canvas.rect(0, -self.hg, self.wd, self.hg)
        
        # fuente
        self.canvas.setFont(self.report.font.name, self.report.font.size)
        
        # imprimir page_header de la página actual
        if self.cur_page.page_header != None:            
            self.writePageHeader(self.cur_page.page_header)
        
    def writeReport(self, pdf_file, c=None, params=None, debug=False):
        
        self.debug = debug
        
        # canvas
        if c != None:
            self.canvas = c
        else:
            self.canvas = canvas.Canvas(pdf_file, pagesize=A4)
      
        # cargar fuentes
        vera_f = TTFont('VeraSans', 'C:/WINDOWS/Fonts/Vera.ttf')
        tahoma_f = TTFont('Tahoma', 'C:/WINDOWS/Fonts/Tahoma.ttf')
        lucida_f = TTFont('LucidaSans', 'C:/WINDOWS/Fonts/lsans.ttf')
        pdfmetrics.registerFont(vera_f)
        pdfmetrics.registerFont(tahoma_f)
        pdfmetrics.registerFont(lucida_f)
        
        param_names = [param[0] for param in self.report.params.params]
            
        # params
        if params != None:
            for p in params:
                if p[0] in param_names:
                    i = param_names.index(p[0])
                    self.report.params.params[i] = p
           
        self.cur_page = self.report.pages[0]
        self.newPage()
        primera_pagina = True
        
        # title
        self.writeReportTitle(self.report.title)
        
        # pages
        for page in self.report.pages:
            self.cur_page = page
            if not primera_pagina:
                self.newPage()
                
            self.writeReporPage(page)
            self.canvas.showPage()
            
            primera_pagina = False
            
        self.canvas.save()
    
    def writeReportTitle(self, title):
        self.writeBody(title.body, 0)
    
    def writeReporPage(self, page):
        
        if self.debug: print 'ReportPage:', str(page)
        
#        # page_header
#        if page.page_header != None:
#            self.writePageHeader(page.page_header, 0)
            
        # body
        self.writeBody(page.body, 0)
        
        # page_footer
        if page.page_footer != None:
            self.writePageFooter(page.page_footer)
    
    def writeBody(self, body, y, mdata=None, ddata=None):
                
        # averiguar si todos los elementos son "Text" o no
        only_text = True
        for item in body.items:
            if not isinstance(item, reports.Text):
                only_text = False
                break
                    
        min_y = y
        new_page = False          
        y0 = y  
        if only_text:
            
#            print '***POSICIONAL***'
            
            # posicional
            # cada elemento tiene una posición predefinida
            
            text_items = []
            text_items_next_page = []
            for item in body.items:
                y, new_page = self.getTextHeight(item, y0)
                if new_page:
                    text_items_next_page.append((item, y))
                else:
                    text_items.append(item)
                    
            if new_page and not body.split_on_new_page:
                self.canvas.showPage()
                self.newPage()                
                min_y = 0
                y0 = 0
                    
            # en esta página
            for item in text_items:
                y, new_page = self.writeText(item, y0, mdata, ddata)
                if y < min_y: min_y = y                
            
            if text_items_next_page != []:
                # crear nueva página
                new_page = True
                if body.split_on_new_page:
                    self.canvas.showPage()
                    self.newPage()
                min_y = 0
            
                # en la siguiente página
                for item, y in text_items_next_page:
                    y = self.writeText(item, 0, mdata, ddata)[0]
                    if y < min_y: min_y = y
                
            return min_y, new_page
                
        else:
#            print '***ACUMULATIVA***'
            
            # acumulativa
            # la posición de un elemento depende de todos los anteriores
            
            for item in body.items:
                # Master
                if isinstance(item, reports.Master):
                    y, new_page = self.writeMaster(item, y)
                
                # Text
                elif isinstance(item, reports.Text):
                    y, new_page = self.writeText(item, y, mdata, ddata)
                
                # Line
#                elif isinstance(item, reports.Line):
#                    y = self.writeLine(item, y)
                
                if not new_page:
                    if y < min_y: min_y = y
                else:
                    min_y = y
            
        return min_y, new_page    
    
    def writeMaster(self, master, y):
        
        sql = master.table.query
        
        # parámetros
        master_dict = {}
        for par in self.report.params.params:
            if sql.find(par[0]):
                master_dict[par[0]] = par[1]
                
        if master_dict != {}:
            sql %= master_dict
            
        # group headers
        primero = True
        min_y = y
        new_page = False
        values = [None] * len(master.group_headers)
        for mdata in self.conector.conexion.execute(sql):

            i = 0
            for i in xrange(len(master.group_headers)):
                if mdata[master.group_headers[i].field] != values[i]:
                    if not primero and master.group_headers[i].options.print_on_new_page:
                        self.canvas.showPage()
                        self.newPage()
                        y = 0
                        min_y = y
                        
                    primero = False
                        
                    y, new_page = self.writeBody(master.group_headers[i].header, y, mdata)
                    values[i] = mdata[master.group_headers[i].field]
                    
                    if not new_page:
                        if y < min_y: min_y = y
                    else:
                        min_y = y
                
                i += 1
            
            # master:body
            y, new_page = self.writeBody(master.body, y, mdata)
            if not new_page:
                if y < min_y: min_y = y
            else:
                min_y = y
            
            # master:detail
            for detalle in master.details:
                y, new_page = self.writeDetail(detalle, y, mdata)
                
                if not new_page:
                    if y < min_y: min_y = y
                else:
                    min_y = y
                
        return min_y, new_page        
    
    def writeDetail(self, detail, y, mdata):

        # tratar SQL
        detail_dict = {}
        detail_dict[detail.master_field] = mdata[detail.master_field]       
        
        sql = detail.table.query
        
        # parámetros 
        for par in self.report.params.params:
            if sql.find(par[0]):
                detail_dict[par[0]] = par[1]
                
        sql %= detail_dict
        
        data = self.conector.conexion.execute(sql)

        min_y = y
        new_page = False
        
        # detail:header
        if detail.header != None:
            if data.rowcount > 0:
                y, new_page = self.writeBody(detail.header.body, y, mdata)            
            else:
                if detail.header.print_if_detail_is_empty:
                    y, new_page = self.writeBody(detail.header.body, y, mdata)
                    
            if not new_page:
                if y < min_y: min_y = y
            else:
                min_y = y      
        
        for ddata in data:
            y, new_page = self.writeBody(detail.body, y, mdata, ddata)
            if not new_page:
                if y < min_y: min_y = y
            else:
                min_y = y
            
        return min_y, new_page
    
    def writePageHeader(self, page_header):
        self.canvas.saveState()
        self.canvas.translate(0, page_header.height * mm)
        self.canvas.rect(0, 0, self.wd, -page_header.height * mm)        
        self.writeBody(page_header.body, 0)
        self.canvas.restoreState()
    
    def writePageFooter(self, page_footer):
        pass
    
    def writeGroupHeader(self, group_header, y, data):
        field_value = None
        min_y = y
        new_page = False
        for mdata in data:
            if mdata[group_header.field] != field_value:
                y, new_page = self.writeBody(group_header.header, y, mdata) #, ddata)
                field_value = mdata[group_header.field]
                
            y, new_page = self.writeBody(group_header.body, y, mdata)
            
            if not new_page:
                if y < min_y: min_y = y
            else:
                min_y = y
                
        return min_y, new_page
    
    def writeGroupFooter(self, group_footer):
        pass
    
    def getTextHeight(self, text, y):
        new_page = False
        y -= (text.top * mm + text.height * mm)
        if y < -self.hg:
            y = y + self.hg # y = y - (-self.hg)
            new_page = True
            
        return y, new_page    
    
    def writeText(self, text, y, mdata=None, ddata=None):
        
        out = text.value
        
        # master
        if mdata != None:
            for k in mdata.keys():
                k2 = '#%s#' % str(k)
                out = out.replace(k2, str(mdata[k]))

        # detail
        if ddata != None:
            for k in ddata.keys():
                k2 = '#%s#' % str(k)
                out = out.replace(k2, str(ddata[k]))

        # params
        for par in self.report.params.params:
            k2 = '#%s#' % par[0]
            out = out.replace(k2, par[1])
        
        # imprimir contenido por "stdout"
        if self.debug: print out, y - (text.top * mm + text.height * mm), text.top, text.height

        sz = self.report.font.size
        if text.font.size != None:
            sz = text.font.size
            
        fn = self.report.font.name
        if text.font.name != None:
            fn = text.font.name
            
        new_page = False
        y -= (text.top * mm + text.height * mm)
        if y < -self.hg:
            self.canvas.showPage()
            self.newPage()
            y = -(text.top * mm + text.height * mm)
            new_page = True
        
        # guardar estado            
        self.canvas.saveState()
        
        # cambiar fuente
        self.canvas.setFont(fn, sz)
        if text.font.color != None:
            r = int(text.font.color[0:2], 16) / 255.0
            g = int(text.font.color[2:4], 16) / 255.0
            b = int(text.font.color[4:6], 16) / 255.0
            self.canvas.setFillColorRGB(r, g, b)
            
        elif self.report.font.color != None:
            r = int(self.report.font.color[0:2], 16) / 255.0
            g = int(self.report.font.color[2:4], 16) / 255.0
            b = int(self.report.font.color[4:6], 16) / 255.0
            self.canvas.setFillColorRGB(r, g, b)
        
        self.canvas.drawString(text.left * mm, y, out)
        
#        self.canvas.setStrokeColorRGB(r, g, b)
#        self.canvas.line(0, y, self.wd, y)
        
        # restaurar estado
        self.canvas.restoreState()
        
        return y, new_page
    
    def writeLine(self, line, y):
        
        if self.debug: 
            print 'Line: x1=%d, y1=%d, x2=%d, y2=%d' % \
                (line.x1, line.y1, line.x2, line.y2)
        
        self.canvas.saveState()
        self.canvas.translate(0, y)
        self.canvas.line(line.x1, line.y1, line.x2, line.y2)
        self.canvas.restoreState()
        
        min_y = y
        if line.y1 < min_y: min_y = line.y1
        if line.y2 < min_y: min_y = line.y2
        
        return min_y
    