# -*- coding: utf-8 -*-

import reports
import cStringIO

class ReportPlainText(object):
    
    def __init__(self, report, conector):
        self.report = report
        self.conector = conector
        self.ftext = cStringIO.StringIO()
        self.debug = False
        
    def writeReport(self, text_file=None, params=None, debug=False):
        
        self.debug = debug
        
        param_names = [param[0] for param in self.report.params.params]
            
        # params
        if params != None:
            for p in params:
                if p[0] in param_names:
                    i = param_names.index(p[0])
                    self.report.params.params[i] = p
           
        self.cur_page = self.report.pages[0]
                
        # title
        self.writeReportTitle(self.report.title)
        
        # pages
        for page in self.report.pages:
            self.cur_page = page                
            self.writeReporPage(page)
             
        # guardar cambios en 'text_file'
        if text_file != None:
            f = file(text_file, 'w')
            try:
                self.ftext.seek(0)
                f.write(self.ftext.read())
            
            finally:
                f.close()
                
        self.ftext.seek(0)
        return self.ftext.read() 
    
    def writeReportTitle(self, title):
        self.writeBody(title.body, 0)
    
    def writeReporPage(self, page):
        
        if self.debug: print 'ReportPage:', str(page)
        
#        # page_header
#        if page.page_header != None:
#            self.writePageHeader(page.page_header, 0)
            
        # body
        self.writeBody(page.body)
        
        # page_footer
        if page.page_footer != None:
            self.writePageFooter(page.page_footer)
    
    def writeBody(self, body, mdata=None, ddata=None):
                
        for item in body.items:
            # Master
            if isinstance(item, reports.Master):
                self.writeMaster(item)
                
            elif isinstance(item, reports.Detail):
                self.writeDetail(item, mdata)
            
            # Text
            elif isinstance(item, reports.Text):
                self.writeText(item, mdata, ddata)
                
            # TextFile
            elif isinstance(item, reports.TextFile):
                self.writeTextFile(item, mdata, ddata)                
            
    def writeMaster(self, master):
        
        sql = master.table.query
        
        # parámetros
        master_dict = {}
        for par in self.report.params.params:
            if sql.find(par[0]):
                master_dict[par[0]] = par[1]
                
        if self.debug: print 'master_dict =', master_dict
                
        if master_dict != {}:
            sql %= master_dict
            
        if self.debug: print sql
            
        values = [None] * len(master.group_headers)
        for mdata in self.conector.conexion.execute(sql):
            
            i = 0
            for i in xrange(len(master.group_headers)):
                if mdata[master.group_headers[i].field] != values[i]:
                    self.writeBody(master.group_headers[i].header, mdata)
                    values[i] = mdata[master.group_headers[i].field]
                                    
                i += 1
            
            # master:body
            self.writeBody(master.body, mdata)
            
            # master:detail
            for detalle in master.details:
                self.writeDetail(detalle, mdata)        
    
    def writeDetail(self, detail, mdata):

        # tratar SQL
        detail_dict = {}
        detail_dict[detail.master_field] = mdata[detail.master_field]       
        
        sql = detail.table.query
        
        # parámetros 
        for par in self.report.params.params:
            if sql.find(par[0]):
                detail_dict[par[0]] = par[1]
                
        sql %= detail_dict
        
        if self.debug: print sql
        
        for ddata in self.conector.conexion.execute(sql):
            self.writeBody(detail.body, mdata, ddata)
    
    def writePageHeader(self, page_header):
        self.writeBody(page_header.body)
    
    def writePageFooter(self, page_footer):
        pass
    
    def writeGroupHeader(self, group_header, y, data):
        field_value = None
        for mdata in data:
            if mdata[group_header.field] != field_value:
                self.writeBody(group_header.header, mdata) #, ddata)
                field_value = mdata[group_header.field]
                
            self.writeBody(group_header.body, mdata)
                
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
        
        # imprimir contenido por "stdout"
        if self.debug: print out
        
        self.ftext.write(out + '\n')
        
    def writeTextFile(self, textfile, mdata=None, ddata=None):
        
        ft = file(textfile.path, 'r')
        try:
            out = ft.read()
        finally:
            ft.close()
        
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
        if self.debug: print out
        
        self.ftext.write(out + '\n')        