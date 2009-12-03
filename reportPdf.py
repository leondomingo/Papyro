# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
import reportlab.lib.pagesizes as pagesizes
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportBase import ReportBase
import reports
import os.path
import sys

class ReportPdf(ReportBase):
    
    def __init__(self, report, conector):
        ReportBase.__init__(self, report, conector)
        self.canvas = None
        self.wd0 = 0
        self.hg0 = 0
        self.hg = 0
        self.wd = 0
        self.cur_page = None
        
        sys.path.append(self.report.path)
        
        # scripts
        for sc in self.report.scripts:
            #prueba = __import__('prueba', globals(), locals())
            global PaCODE
            PaCODE = __import__(os.path.splitext(sc.file)[0], globals(), locals())        
        
    def newPage(self, save=False):
        
        if save:
            # page_footer        
            if self.cur_page.page_footer != None:
                self.writePageFooter(self.cur_page.page_footer)
                
            self.canvas.showPage()        
        
        if self.debug: print '***NEW PAGE*****************'
        
        self.page_no += 1
        
        # margin
        m_left = self.report.margin_left * mm
        m_right = self.report.margin_right * mm
        m_top = self.report.margin_top * mm
        m_bottom = self.report.margin_bottom * mm
                
        # page_header height
        ph_height = 0
        if self.cur_page.page_header != None:
            ph_height = self.cur_page.page_header.height * mm
            
        # page_footer height
        pf_height = 0
        if self.cur_page.page_footer != None:
            pf_height = self.cur_page.page_footer.height * mm
            
        # width with margins
        self.wd = self.wd0 - m_left - m_right
        self.hg = self.hg0 - m_top - m_bottom - ph_height - pf_height
        
        # "translate" origin
        self.canvas.translate(m_left, self.hg + m_bottom + pf_height)
        
        # draw margins
        if self.debug: self.canvas.rect(0, -self.hg, self.wd, self.hg)
        
        # font
        self.canvas.setFont(self.report.font.name, self.report.font.size)
        
        # print "page_header" of the current page
        if self.cur_page.page_header != None:            
            self.writePageHeader(self.cur_page.page_header)
        
    def writeReport(self, pdf_file, c=None, params=None, debug=False):
        
        self.debug = debug
        
        # canvas
        if c != None:
            # using an external 'canvas'
            self.canvas = c
            
        else:
            # typical paper sizes
            
            if self.report.paper_size == 'A0':
                paper_size = pagesizes.A0
                
            elif self.report.paper_size == 'A1':
                paper_size = pagesizes.A1

            elif self.report.paper_size == 'A2':
                paper_size = pagesizes.A2 

            elif self.report.paper_size == 'A3':
                paper_size = pagesizes.A3

            elif self.report.paper_size == 'A4':
                paper_size = pagesizes.A4

            elif self.report.paper_size == 'A5':
                paper_size = pagesizes.A5
                
            elif self.report.paper_size == 'LETTER':
                paper_size = pagesizes.letter
                
            else:
                paper_size = pagesizes.A4
                
            # orientation
            if self.report.paper_orientation.lower() == 'landscape':
                self.wd0 = paper_size[1]
                self.hg0 = paper_size[0]
                
            else:
                # portrait
                self.wd0 = paper_size[0]
                self.hg0 = paper_size[1]
                
            self.canvas = canvas.Canvas(pdf_file, pagesize=(self.wd0 , self.hg0))
        
        # load fonts
        base = os.path.dirname(__file__)
        pdfmetrics.registerFont(TTFont('VeraSans', os.path.join(base, 'ttfonts/vera.ttf')))
        pdfmetrics.registerFont(TTFont('Tahoma', os.path.join(base, 'ttfonts/tahoma.ttf')))
        pdfmetrics.registerFont(TTFont('LucidaSans', os.path.join(base, 'ttfonts/lsans.ttf')))
        pdfmetrics.registerFont(TTFont('Arial', os.path.join(base, 'ttfonts/arial.ttf')))
        pdfmetrics.registerFont(TTFont('TimesNewRoman', os.path.join(base, 'ttfonts/times.ttf')))
        pdfmetrics.registerFont(TTFont('CourierNew', os.path.join(base, 'ttfonts/couriernew.ttf')))
        pdfmetrics.registerFont(TTFont('Georgia', os.path.join(base, 'ttfonts/georgia.ttf')))
        pdfmetrics.registerFont(TTFont('Verdana', os.path.join(base, 'ttfonts/verdana.ttf')))
        pdfmetrics.registerFont(TTFont('MsSanSerif', os.path.join(base, 'ttfonts/msanserif.ttf')))
        
        # get param names
        param_names = [param[0] for param in self.report.params.params]
            
        # params
        if params != None:
            for p in params:
                if p[0] in param_names:
                    i = param_names.index(p[0])
                    self.report.params.params[i] = p
           
        self.cur_page = self.report.pages[0]
        self.newPage()
        first_page = True        
        
        # title
        self.writeReportTitle(self.report.title)
                
        # pages
        for page in self.report.pages:
            self.cur_page = page
            if not first_page:
                self.newPage(save=True)
                
            self.writeReporPage(page)
            self.canvas.showPage()
            
            first_page = False
                        
        self.canvas.save()
    
    def writeReportTitle(self, title):
        self.writeBody(title.body, 0)
    
    def writeReporPage(self, page):
        
        if self.debug: print 'ReportPage:', str(page)
            
        # body
        self.writeBody(page.body, 0)
        
        # page_footer
        if page.page_footer != None:
            self.writePageFooter(page.page_footer)                
    
    def writeBody(self, body, y, mdata=None, ddata=None):

        # check "print_if" condition
        if not self.check_condition(body.print_if, mdata, ddata):
            return y, False            
                
        # all the items are "Text"?
        only_text = True
        for item in body.items:            
            if not isinstance(item, reports.Text) and \
            not isinstance(item, reports.Image) and \
            not isinstance(item, reports.Line) and \
            not isinstance(item, reports.Code):
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
                if not isinstance(item, reports.Code):
                    y, new_page = self.getTextHeight(item, y0)
                    if new_page:
                        text_items_next_page.append((item, y))
                    else:
                        text_items.append(item)
                        
                else:
                    # execute "code"
                    self.execute_code(item)
                    
            if new_page and not body.split_on_new_page:
                self.newPage(save=True)                
                min_y = 0
                y0 = 0
                    
            # on this page
            for item in text_items:
                if isinstance(item, reports.Text):
                    y, new_page = self.writeText(item, y0, mdata, ddata)
                    
                elif isinstance(item, reports.Image):
                    y, new_page = self.writeImage(item, y0)
                    
                elif isinstance(item, reports.Line):
                    y = self.writeLine(item, y0)
                    
                if y < min_y: min_y = y                
            
            if text_items_next_page != []:
                # crear nueva página
                new_page = True
                if body.split_on_new_page:
                    self.newPage(save=True)
                min_y = 0
            
                # on the next page
                for item, y in text_items_next_page:
                    if isinstance(item, reports.Text):
                        y = self.writeText(item, 0, mdata, ddata)[0]
                    
                    elif isinstance(item, reports.Image):
                        y = self.writeImage(item, 0)[0]    

                    elif isinstance(item, reports.Line):
                        y = self.writeLine(item, 0)
                    
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
                    
                # Image
#                elif isinstance(item, reports.Image):
#                    y, new_page = self.writeImage(item, y)
                
                if not new_page:
                    if y < min_y: min_y = y
                else:
                    min_y = y
            
        return min_y, new_page    
    
    def writeMaster(self, master, y):
        
        sql = master.table.query
        
        # parameters
        master_dict = {}
        for par in self.report.params.params:
            if sql.find(par[0]):
                master_dict[par[0]] = par[1]
                
        if master_dict != {}:
            sql %= master_dict
            
        # group headers
        first_gh = True
        min_y = y
        new_page = False
        values = [None] * len(master.group_headers)
        footers = []
        for gh in master.group_headers:            
            # find the "footer" for this "header"
            footer = None
            for gf in master.group_footers:
                if gf.id == gh.footer_id:                    
                    footer = gf
                    break
                    
            footers.append(footer)
        
        data = self.conector.conexion.execute(sql).fetchall()
        n = 0           
        for mdata in data:
            for i in xrange(len(master.group_headers)):
                if mdata[master.group_headers[i].field] != values[i]:
                    if not first_gh and master.group_headers[i].options.print_on_new_page:
                        self.newPage(save=True)
                        y = 0
                        min_y = y
                        
                    first_gh = False
                    
                    # group_header    
                    y, new_page = self.writeBody(master.group_headers[i].header, y, mdata)
                    values[i] = mdata[master.group_headers[i].field]
                    
                    if not new_page:
                        if y < min_y: min_y = y
                    else:
                        min_y = y
            
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

            for i in xrange(len(master.group_headers) - 1, -1, -1):
                # exists next record?
                if len(data) > (n + 1):
                    next_value = data[n + 1][master.group_headers[i].field]
                else:
                    # there's no "next" record
                    next_value = None
                    
                if next_value != values[i]:
                    # group_footer, if any
                    if footers[i] != None:
                        y, new_page = self.writeBody(footers[i].footer, y, mdata)
                        
                        if not new_page:
                            if y < min_y: min_y = y
                        else:
                            min_y = y
                                                                            
            n += 1
                
        return min_y, new_page        
    
    def writeDetail(self, detail, y, mdata):

        # manage SQL
        detail_dict = {}
        detail_dict[detail.master_field] = mdata[detail.master_field]       
        
        sql = detail.table.query
        
        # parameters 
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
        if self.debug: self.canvas.rect(0, 0, self.wd, -page_header.height * mm)        
        self.writeBody(page_header.body, 0)
        self.canvas.restoreState()
    
    def writePageFooter(self, page_footer):
        self.canvas.saveState()
        self.canvas.translate(0, -self.hg)        
        if self.debug: self.canvas.rect(0, 0, self.wd, -page_footer.height * mm)                    
        self.writeBody(page_footer.body, 0)
        self.canvas.restoreState()
    
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
        
        # check "print_if" condition
        if not self.check_condition(text.print_if, mdata, ddata):
            return y, False
        
        out = text.value
        
        # constants        
        out = self.apply_constants(out)
        
        # master
        out = self.apply_data(out, mdata)
        
        # detail
        out = self.apply_data(out, ddata)
        
        # parameters
        out = self.apply_parameters(out)
        
        # code
        out = self.compile_text(out)
        
        # print content thru "stdout"
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
            self.newPage(save=True)
            y = -(text.top * mm + text.height * mm)
            new_page = True
        
        # save state            
        self.canvas.saveState()
        
        # change font
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
        
        # restore state
        self.canvas.restoreState()
        
        return y, new_page
    
    def writeLine(self, line, y):
        
        # check "print_if" condition
        if not self.check_condition(line.print_if):
            return y       
        
        y1 = y
        if line.y1 != None: y1 = y -(line.y1 * mm)
        
        y2 = y
        if line.y2 != None: y2 = y -(line.y2 * mm)
        
#        if self.debug:
#        print 'Line: x1=%2.2f, y1=%2.2f, x2=%2.2f, y2=%2.2f' % \
#            (line.x1 * mm, y1, line.x2 * mm, y2)
        
        self.canvas.line(line.x1 * mm, y1, line.x2 * mm, y2)

        min_y = y
#        if y1 < min_y: min_y = y1
#        if y2 < min_y: min_y = y2
        
        return min_y
    
    def writeImage(self, image, y):
        
        # check "print_if" condition
        if not self.check_condition(image.print_if):
            return y, False
        
        y -= (image.top + image.height) * mm
        
        self.canvas.drawImage(os.path.join(self.report.path, image.filename), image.left * mm, y, 
                              image.width * mm, image.height * mm, 
                              preserveAspectRatio=image.keep_aspect_ratio) #, mask, preserveAspectRatio, anchor
        
        return y, False
    