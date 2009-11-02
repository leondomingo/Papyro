# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import reports
import string
#from random import seed, randint

class ReportPdf(object):
    
    def __init__(self, report, conector):
        self.report = report
        self.conector = conector
        self.canvas = None
        
    def newPage(self):
        
        # margin
        m_left = self.report.margin_left * mm
        m_right = self.report.margin_right * mm
        m_top = self.report.margin_top * mm
        m_bottom = self.report.margin_bottom * mm
        
        # anchura de A4
        wd0 = 210 * mm
        hg0 = 297 * mm
        
        # anchura con márgenes
        self.wd = wd0 - m_left - m_right
        self.hg = hg0 - m_top - m_bottom
        
        # mover origen
        self.canvas.translate(m_left, self.hg + m_bottom)
        
        # dibujar espacio con los márgenes
        self.canvas.rect(0, -self.hg, self.wd, self.hg)
        
        # fuente
        self.canvas.setFont(self.report.font.name, self.report.font.size)
        
    def writeReport(self, file, c=None, params=None):
        
        # canvas
        if c != None:
            self.canvas = c
        else:
            self.canvas = canvas.Canvas(file, pagesize=A4)
            
        param_names = [param[0] for param in self.report.params.params]
            
        # params
        if params != None:
            for p in params:
                if p[0] in param_names:
                    i = param_names.index(p[0])
                    self.report.params.params[i] = p
           
        self.newPage()
        primera_pagina = True
        
        # title
        self.writeReportTitle(self.report.title)
        
        # pages
        for page in self.report.pages:
            if not primera_pagina:
                self.newPage()
                
            self.writeReporPage(page)
            self.canvas.showPage()
            
            primera_pagina = False
            
        self.canvas.save()
    
    def writeReportTitle(self, title):
        self.writeBody(title.body, 0)
    
    def writeReporPage(self, page):
        
        print 'ReportPage:', str(page)
        
        # page_header
        if page.page_header != None:
            self.writePageHeader(page.page_header)       
        
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
                    
            # en esta página
            for item in text_items:
                y, new_page = self.writeText(item, y0, mdata, ddata)
                if y < min_y: min_y = y                
            
            if text_items_next_page != []:
                # crear nueva página
                y = 0
                min_y = y
                new_page = True
                self.canvas.showPage()
                self.newPage()
            
                # en la siguiente página
                for item, y in text_items_next_page:
                    self.writeText(item, y, mdata, ddata)
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
        
        min_y = y
        new_page = False
        for mdata in self.conector.conexion.execute(sql):
            y, new_page = self.writeBody(master.body, y, mdata)
            if new_page: min_y = y
            
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
        
        min_y = y
        new_page = False
        for ddata in self.conector.conexion.execute(sql):
            y, new_page = self.writeBody(detail.body, y, mdata, ddata)
            if not new_page:
                if y < min_y: min_y = y
            else:
                min_y = y
            
        return min_y, new_page
    
    def writePageHeader(self, page_header):
        pass
    
    def writePageFooter(self, page_footer):
        pass
    
    def writeGroupHeader(self, group_header):
        pass
    
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
        print out

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
        
#        r = randint(0, 255) / 255.0
#        g = randint(0, 255) / 255.0
#        b = randint(0, 255) / 255.0
#        self.canvas.setStrokeColorRGB(r, g, b)
#        self.canvas.rect(0, y, self.wd, text.height * mm, stroke=1, fill=0)

        # cambiar fuente
        self.canvas.setFont(fn, sz)
        if text.font.color != None:
            r = string.atoi(text.font.color[0:2], 16) / 255.0
            g = string.atoi(text.font.color[2:4], 16) / 255.0
            b = string.atoi(text.font.color[4:6], 16) / 255.0
            self.canvas.setFillColorRGB(r, g, b)
        
        self.canvas.drawString(text.left * mm, y, out)
        
        # restaurar estado
        self.canvas.restoreState()
        
        return y, new_page
    
    
        