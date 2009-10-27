# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm 
import reports

class ReportPdf(object):
    
    def __init__(self, report, conector):
        self.report = report
        self.conector = conector
        self.canvas = None
        self.cur_y = 0
        
    def newPage(self):
        # margin
        m_left = self.report.margin_left * 10 * mm
        m_right = self.report.margin_right * 10 * mm
        m_top = self.report.margin_top * 10 * mm
        m_bottom = self.report.margin_bottom * 10 * mm
        
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
        
        self.cur_y = 0
        
        # fuente
        self.canvas.setFont(self.report.font.name, self.report.font.size)
        
    def writeReport(self, file, c=None):
        
        # canvas
        if c != None:
            self.canvas = c
        else:
            self.canvas = canvas.Canvas(file, pagesize=A4)
            
        self.newPage()
        
        # title
        self.writeReportTitle(self.report.title)
        
        # pages
        for page in self.report.pages:
            self.writeReporPage(page)
            self.canvas.showPage()
            
        self.canvas.save()
    
    def writeReportTitle(self, title):
        # TODO: hace falta un "origen" desde donde empezar a dibujar
        self.writeBody(title.body)
    
    def writeReporPage(self, page):
        # page_header
        if page.page_header != None:
            self.writePageHeader(page.page_header)       
        
        # body
        # TODO: hace falta un "origen" desde donde empezar a dibujar
        self.writeBody(page.body)
        
        # page_footer
        if page.page_footer != None:
            self.writePageFooter(page.page_footer)
    
    def writeBody(self, body, mdata=None, ddata=None):
        
#        self.canvas.saveState()        
#        self.canvas.translate(body.left, -body.top)
        
        # items
        for item in body.items:
            # Master
            if isinstance(item, reports.Master):
                self.writeMaster(item)
            
            # Label    
            elif isinstance(item, reports.Label):
                self.writeLabel(item, mdata, ddata)
            
            # Text
            elif isinstance(item, reports.Text):
                self.writeText(item, mdata, ddata)
                
#        self.canvas.restoreState()
    
    def writeMaster(self, master):
        
        sql = master.table.query.replace('$$', '<')
        
        # parámetros
        master_dict = {}
        for par in self.report.params.params:
            if sql.find(par[0]):
                master_dict[par[0]] = par[1]
                
        if master_dict != {}:
            sql %= master_dict            
        
        for mdata in self.conector.conexion.execute(sql):
            # TODO: hace falta un "origen" desde donde empezar a dibujar
            self.writeBody(master.body, mdata)
            
            for detalle in master.details:
                self.writeDetail(detalle, mdata)
    
    def writeDetail(self, detail, mdata):

        # tratar SQL
        detail_dict = {}
        detail_dict[detail.master_field] = mdata[detail.master_field]       
        
        sql = detail.table.query.replace('$$', '<')
        
        # parámetros 
        for par in self.report.params.params:
            if sql.find(par[0]):
                detail_dict[par[0]] = par[1]
                
        sql %= detail_dict
        
        for ddata in self.conector.conexion.execute(sql):                        
            # TODO: hace falta un "origen" desde donde empezar a dibujar
            self.writeBody(detail.body, mdata, ddata)
    
    def writePageHeader(self, page_header):
        pass
    
    def writePageFooter(self, page_footer):
        pass
    
    def writeGroupHeader(self, group_header):
        pass
    
    def writeGroupFooter(self, group_footer):
        pass
    
    def writeText(self, text, mdata=None, ddata=None):

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
        
        # TODO: escribir en el PDF
        print out

        sz = self.report.font.size
        if text.font.size != None:
            sz = text.font.size
            
        fn = self.report.font.name
        if text.font.name != None:
            fn = text.font.name
            
        self.cur_y -= (text.top + text.height)
        #self.cur_y -= sz
        if self.cur_y < -self.hg:
            self.canvas.showPage()
            self.newPage()
            self.cur_y = -sz
            
        # guardar estado            
        self.canvas.saveState()

        # cambiar fuente
        self.canvas.setFont(fn, sz)
                        
        self.canvas.drawString(text.left * mm, self.cur_y, out)
        
        # restaurar estado
        self.canvas.restoreState()
            
    def writeLabel(self, label, mdata=None, ddata=None):

        out = label.caption
        
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
                
        # TODO: escribir en el PDF
        print out
        
        self.cur_y -= 12
        if self.cur_y < -self.hg:
            self.canvas.showPage()
            self.newPage()
            self.cur_y = -12

        self.canvas.drawString(10, self.cur_y, out)