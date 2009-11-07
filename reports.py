# -*- coding: utf-8 -*-

from lxml import etree

class Font(object):
    def __init__(self):
        self.name = None
        self.size = None
        self.color = None
        self.style = [False, False, False, False] # bold, italic, underline, strike
    
    def getxml(self):
        valor = \
            '<font>\n' + \
            '  <name>' + (self.name or '') + '</name>\n' + \
            '  <size>' + str(self.size or 0) + '</size>\n' + \
            '  <color>' + (self.color or '') + '</color>\n' + \
            '  <style>\n' + \
            ('    <bold/>' if self.style[0] else '') + \
            ('    <italic/>' if self.style[1] else '') + \
            ('    <underline/>' if self.style[2] else '') + \
            ('    <strike/>' if self.style[3] else '') + \
            '  </style>\n' + \
            '</font>\n'
        return valor
    
    def setxml(self, valor):
        fuente = etree.fromstring(valor)
        
        self.name = fuente.find('name').text
        self.size = int(fuente.find('size').text or 0)
        self.color = fuente.find('color').text
        
        self.style[0] = fuente.find('bold') != None
        self.style[1] = fuente.find('italic') != None
        self.style[2] = fuente.find('underline') != None
        self.style[3] = fuente.find('strike') != None
        
    xml = property(getxml, setxml)
    
class Parameters(object):
    def __init__(self):
        self.params = []
        
    def getxml(self):
        valor = '<params>\n'
        
        for par in self.params:
            # 0 - name
            # 1 - (valor)
            # 2 - type
            valor += '<param name="%s" type="%s">%s</param>\n' % (par[0], par[2], par[1])
                            
        valor += '</params>\n'
        
        return valor        
        
        
    def setxml(self, valor):        
        parametros = etree.fromstring(valor)        
        
        self.params = []
        for param in parametros.iterchildren('param'):
            self.params.append((param.attrib['name'], param.text, param.attrib['type']))
            
    xml = property(getxml, setxml)

class ReportItem(object):
    def __init__(self):
        self.left = 0
        self.top = 0
        self.height = 0
        self.width = 0
        self.font = Font()
    
    def write(self):
        print '(%(lf)d, %(tp)d) (%(hg)d, %(wd)d) ' % \
                    dict(lf=self.left or 0, tp=self.top or 0, 
                         hg=self.height or 0, wd=self.width or 0)
                    
    def getxml(self):
        valor = \
            '  <position>\n' + \
            '    <left>' + str(self.left or 0) + '</left>\n' + \
            '    <top>' + str(self.top or 0) + '</top>\n' + \
            '  </position>\n' + \
            '  <size>\n' + \
            '    <height>' + str(self.height or 0) + '</height>\n' + \
            '    <width>' + str(self.width or 0) + '</width>\n' + \
            '  </size>\n' + \
            self.font.xml
            
        return valor
    
    def setxml(self, valor):
        item = etree.fromstring(valor)
        
        pos = item.find('position')
        if pos != None:
            self.left = int(pos.find('left').text or 0)
            self.top = int(pos.find('top').text or 0)
                
        size = item.find('size')
        if size != None:
            self.height = int(size.find('height').text or 0)
            self.width = int(size.find('width').text or 0)
            
        if item.find('font') != None:
            self.font.xml = etree.tostring(item.find('font'))
        
    xml = property(getxml, setxml)   
        
    
class PrintableItem(ReportItem):
    def __init__(self):
        ReportItem.__init__(self)        

class NotPrintableItem(ReportItem):
    def __init__(self):
        ReportItem.__init__(self)
        
class PageHeaderOptions(object):
    def __init__(self):
        self.print_on_first_page = True
        
    def write(self, conector):
        pass
        
    def getxml(self):
        valor = '<options>\n'
        
        if self.print_on_first_page: valor += '  <print_on_first_page/>\n'
        # TODO: Resto de opciones        
        
        valor += '</options>\n'
            
        return valor
    
    def setxml(self, valor):
        op = etree.fromstring(valor)
        
        self.print_on_first_page = op.find('print_on_first_page') != None
        # TODO: resto de opciones
    
    xml = property(getxml, setxml)   
        
class PageHeader(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()
        self.options = PageHeaderOptions
        
    def write(self, conector, params=None):
        print 'PageHeader "%s"' % self.id
#        ReportItem.write(self)
        self.body.write(conector, params=params)
        
    def getxml(self):
        valor = \
            '<page_header>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            ReportItem.getxml(self) + \
            self.options.xml + \
            self.body.xml + \
            '</page_header>\n'
        return valor
    
    def setxml(self, valor):
        ph = etree.fromstring(valor)
        
        self.id = ph.find('id').text or ''
        
        self.body.xml = etree.tostring(ph.find('body'))
        
        if ph.find('options') != None:
            self.options.xml = etree.tostring(ph.find('options'))
            
        ReportItem.setxml(self, valor)
    
    xml = property(getxml, setxml)
    
class PageFooter(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()
    
    def write(self, conector, params=None):
        print 'PageFooter "%s"' % self.id
#        ReportItem.write(self)
        self.body.write(conector, params=params)
        
    def getxml(self):
        valor = \
            '<page_footer>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            ReportItem.getxml(self) + \
            self.body.xml + \
            '</page_footer>\n'
            
        return valor
    
    def setxml(self, valor):
        pf = etree.fromstring(valor)
        
        self.id = pf.find('id').text or ''
        self.body.xml = etree.tostring(pf.find('body'))
        
    xml = property(getxml, setxml)
    
class GroupHeader(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.field = None
        self.header = Header()
        
    def write(self, conector):
        print 'GroupHeader "%s"' % self.id
#        ReportItem.write(self)
        self.body.write(conector)
        
    def getxml(self):
        valor = \
            '<group_header>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            '  <field>' + (self.field or '') + '</field>\n' + \
            ReportItem.getxml(self) + \
            self.header.xml + \
            '</group_header>\n'
            
        return valor
    
    def setxml(self, valor):
        gh = etree.fromstring(valor)
        
        self.id = gh.find('id').text or ''
        self.field = gh.find('field').text or ''
        self.header.xml = etree.tostring(gh.find('header'))
        
    xml = property(getxml, setxml)
    
class GroupFooter(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.footer = Body()   

    def write(self, c, conector):
        print 'GroupFooter "%s"' % self.id
#        ReportItem.write(self)
        self.body.write(conector)

    def getxml(self):
        valor = \
            '<group_footer>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            ReportItem.getxml(self) + \
            self.footer.xml + \
            '</group_footer>\n'
            
        return valor
    
    def setxml(self, valor):
        gf = etree.fromstring(valor)
        
        self.id = gf.find('id').text or ''
        self.body.xml = etree.tostring(gf.find('body'))
        
    xml = property(getxml, setxml)
        
class Table(NotPrintableItem):
    def __init__(self):
        self.query = None
        self.fields = []
        self.body = Body()
        
    def getxmlfields(self):
        valor = '<fields>\n'
        for fld in self.fields:
            valor += '<field>' + fld + '</field>\n'
            
        valor += '</fields>\n'
            
        return valor
    
    def getxml(self):
        valor = \
            '<table>\n' + \
            '  <query>' + self.query + '</query>\n' + \
            self.getxmlfields() + \
            self.body.xml + \
            '</table>\n'
        return valor
    
    def setxml(self, valor):
        tabla = etree.fromstring(valor)
        
        self.query = tabla.find('query').text
        
        self.fields = []
        for fld in tabla.find('fields').iterchildren('field'):
            self.fields.append(fld.text)
        
    xml = property(getxml, setxml)
    
class Detail(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)        
        self.id = id
        self.master_field = None
        self.table = Table()
        self.body = Body()
        
    def write(self, conector, master_data, params):
        print 'Detail "%s" (%s)' % (self.id, self.master_field)
#        ReportItem.write(self)

        # tratar SQL
        detail_dict = {}
        detail_dict[self.master_field] = master_data[self.master_field]       
        
        sql = self.table.query #.replace('$$', '<')
        
        # parámetros 
        for par in params.params:
            if sql.find(par[0]):
                detail_dict[par[0]] = par[1]
                
        sql %= detail_dict
        
        for detail_data in conector.conexion.execute(sql):
            # TODO: Imprimir detalle si está vacío (opcional)
            if detail_data != None:
                self.body.write(conector, master_data, detail_data)
        
    def getxml(self):
        valor = \
            '<detail>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            '  <master_field>' + (self.master_field or '') + '</master_field>\n' + \
            self.table.xml + \
            self.body.xml + \
            '</detail>\n'
            
        return valor
    
    def setxml(self, valor):
        detail = etree.fromstring(valor)
        
        self.id = detail.find('id').text or ''
        self.master_field = detail.find('master_field').text
        self.table.xml = etree.tostring(detail.find('table'))
        self.body.xml = etree.tostring(detail.find('body'))
    
    xml = property(getxml, setxml)
    
class Master(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.table = Table()
        self.group_headers = []
        self.group_footers = []
        self.body = Body()
        self.details = []
        
    def write(self, conector, params):
        print 'Master "%s"' % self.id
        #ReportItem.write(self)
        
        sql = self.table.query #.replace('$$', '<')
        
        # parámetros
        master_dict = {}
        for par in params.params:
            if sql.find(par[0]):
                master_dict[par[0]] = par[1]
                
        if master_dict != {}:
            sql %= master_dict            
        
        for master_data in conector.conexion.execute(sql):
            self.body.write(conector, master_data, params=params)
            
            for detalle in self.details:
                detalle.write(conector, master_data, params)
                
    def getxmldetails(self):
        valor = ''
        for dt in self.details:
            valor += dt.xml
            
        return valor
    
    def getxmlgroupheaders(self):
        valor = ''
        for gh in self.group_headers:
            valor += gh.xml
            
        return valor
    
    def getxmlgroupfooters(self):
        valor = ''
        for gf in self.group_footers:
            valor += gf.xml
            
        return valor

    def getxml(self):
        valor = \
            '<master>\n' + \
            self.table.xml + \
            self.getxmlgroupheaders() + \
            self.getxmlgroupfooters() + \
            self.body.xml + \
            self.getxmldetails() + \
            '</master>\n'
        
        return valor
    
    def setxml(self, valor):
        master = etree.fromstring(valor)
        
        self.id = master.find('id').text or ''
        self.table.xml = etree.tostring(master.find('table'))
        
        # group headers
        self.group_headers = []
        for gh in master.iterchildren('group_header'):
            group_header = GroupHeader()
            group_header.xml = etree.tostring(gh)
            
            self.group_headers.append(group_header)
            
        # group footers
        self.group_footers = []
        for gf in master.iterchildren('group_footer'):
            group_footer = GroupFooter()
            group_footer.xml = etree.tostring(gf)
            
            self.group_footers.append(group_footer)
            
        self.body.xml = etree.tostring(master.find('body'))
        
        self.details = []
        for detalle in master.iterchildren('detail'):
            detail = Detail()
            self.details.append(detail)
            detail.xml = etree.tostring(detalle)
        
    xml = property(getxml, setxml)       
    
        
class Text(PrintableItem):
    def __init__(self, id=None):
        PrintableItem.__init__(self)        
        self.id = id or ''
        self.value = None
        
    def __repr__(self):
        return '"%s" = "%s"' % (self.id, self.value or '')
        
    def write(self, master=None, detail=None, params=None):

        out = self.value
        if master != None:
            for k in master.keys():
                k2 = '#' + str(k) + '#'
                out = out.replace(k2, str(master[k]))
                
        if detail != None:
            for k in detail.keys():
                k2 = '#' + str(k) + '#'
                out = out.replace(k2, str(detail[k]))
                
        if params != None:
            for par in params.params:
                k2 = '#%s#' % par[0]
                out = out.replace(k2, par[1])
                
        print out

    def getxml(self):
        valor = \
            '<text>\n' + \
            '  <id>' + self.id + '</id>\n' + \
            '  <value>' + (self.value or '') + '</value>\n' + \
            ReportItem.getxml(self) + \
            '</text>\n'
            
        return valor
    
    def setxml(self, valor):
        
        texto = etree.fromstring(valor)
        
        self.id = texto.find('id').text or ''
        self.value = texto.find('value').text or ''        
            
        ReportItem.setxml(self, valor)
            
    xml = property(getxml, setxml)

class Body(NotPrintableItem):
    def __init__(self):
        NotPrintableItem.__init__(self)        
        self.items = [] # lista de "ReportItem"
        
    def write(self, conector, master=None, detail=None, params=None):
        
        for item in self.items:
            if isinstance(item, Master):
                item.write(conector, params)
            else:
                # Label, Text, etc
                item.write(master, detail, params)
            
    def getxmlitems(self):
        valor = ''
        for item in self.items:
            valor += item.xml
            
        return valor            
            
    def getxml(self):
        valor = \
            '<body>\n' + \
            self.getxmlitems() + \
            '</body>\n'
            
        return valor
    
    def setxml(self, valor):        
        self.items = []
        cuerpo = etree.fromstring(valor)
        
        for rep_item in cuerpo.iterchildren():
            
            if rep_item.tag == 'text':
                txt = Text()
                self.items.append(txt)
                
                txt.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'master':
                mas = Master()
                self.items.append(mas)
                
                mas.xml = etree.tostring(rep_item)
                
    xml = property(getxml, setxml)
    
class Header(Body):
    def __init__(self):
        Body.__init__(self)
        
    def getxml(self):
        valor = \
            '<header>\n' + \
            Body.getxmlitems(self) + \
            '</header>\n'
            
        return valor
    
    def setxml(self, valor):
        Body.setxml(self, valor)        
                
    xml = property(getxml, setxml)            

class ReportPage(object):
    def __init__(self, id, num=None):
        self.body = Body()
        self.num = num or 1
        self.id = id
        self.page_header = None
        self.page_footer = None
        
    def __repr__(self):
        return '"%s" (page=%d)' % (self.id, self.num)
        
    def write(self, conector, params):
        print 'ReportPage "%s" %d' % (self.id, self.num)
        
        if self.page_header != None:
            self.page_header.write(conector, params=params)
            
        self.body.write(conector, params=params)
        
        if self.page_footer != None:
            self.page_footer.write(conector, params=params)
        
    def getxml(self):
        valor = \
            '<page>\n' + \
            '  <id>' + self.id + '</id>\n' + \
            '  <number>' + str(self.num) + '</number>\n' + \
            (self.page_header.xml if self.page_header != None else '') + \
            self.body.xml + \
            (self.page_footer.xml if self.page_footer != None else '') + \
            '</page>\n'
            
        return valor
    
    def setxml(self, valor):        
        pagina = etree.fromstring(valor)
        
        self.id = pagina.find('id').text or ''
        self.num = int(pagina.find('number').text) or 1
        
        body = pagina.find('body')
        if body != None:
            self.body.xml = etree.tostring(body)
            
        if pagina.find('page_header') != None:
            self.page_header = PageHeader()
            self.page_header.xml = etree.tostring(pagina.find('page_header'))
            
        if pagina.find('page_footer') != None:
            self.page_footer = PageFooter()
            self.page_footer.xml = etree.tostring(pagina.find('page_footer')) 
        
    xml = property(getxml, setxml)
        
class ReportTitle(NotPrintableItem):
    def __init__(self, id):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()
        
    def __repr__(self):
        return '"%s"' % self.id
        
    def write(self, conector):
        print 'ReportTitle "%s"' % self.id
        self.body.write(conector)
        
    def getxml(self):
        valor = \
            '  <report_title>\n' + \
            '    <id>' + self.id + '</id>\n' + \
            ReportItem.getxml(self) + \
            '  </report_title>\n'
        return valor
    
    def setxml(self, valor):
        titulo = etree.fromstring(valor)
        
        self.id = titulo.find('id').text or ''
        
        ReportItem.setxml(self, valor)
        
    xml = property(getxml, setxml)
        

class Report(object):    
    def __init__(self, name=None, xml=None):
        self.name = name or ''        
        self.pages = [] # lista de "ReportPage"
        self.title = ReportTitle(None)
        self.paper_size = None
        self.paper_orientation = None
        self.margin_left = None
        self.margin_right = None
        self.margin_top = None
        self.margin_bottom = None
        self.font = Font()
        self.params = Parameters()
        
        self.xml = xml
        
    def __repr__(self):
        return '"%s" (with %d pages)' % (self.name, len(self.pages))
        
    def getxmlpages(self):
        valor = ''
        for page in self.pages:
            valor += page.xml
            
        return valor
        
    def getxml(self):        
        resultado = \
            '<?xml version="1.0"?>\n' + \
            '<report>\n' + \
            '  <name>' + self.name + '</name>\n' + \
            '  <configuration>\n' + \
            '    <paper>\n' + \
            '      <size>' + (self.paper_size or '') + '</size>\n' + \
            '      <orientation>' + (self.paper_orientation or '') + '</orientation>\n' + \
            '      <margin>\n' + \
            '        <left>' + str(self.margin_left or 0) + '</left>\n' + \
            '        <right>' + str(self.margin_right or 0) + '</right>\n' + \
            '        <top>' + str(self.margin_top or 0) + '</top>\n' + \
            '        <bottom>' + str(self.margin_bottom or 0) + '</bottom>\n' + \
            '      </margin>\n' + \
            '    </paper>\n' + \
            '  </configuration>\n' + \
            self.font.xml + \
            self.params.xml + \
            self.title.xml + \
            self.getxmlpages() + \
            '</report>\n'
            
        return resultado                    
    
    def setxml(self, valor):
        informe = etree.fromstring(valor)
        
        self.name = informe.find('name').text
        
        if informe.find('font') != None:
            self.font.xml = etree.tostring(informe.find('font'))
         
        self.params.xml = etree.tostring(informe.find('params'))
        
        paper = informe.find('configuration').find('paper')
        self.paper_size = paper.find('size').text.upper()
        self.paper_orientation = paper.find('orientation').text.lower()
        
        margin = paper.find('margin')
        self.margin_left = float(margin.find('left').text)
        self.margin_right = float(margin.find('right').text)
        self.margin_top = float(margin.find('top').text)
        self.margin_bottom = float(margin.find('bottom').text)
        
        rt = informe.find('report_title')
        if rt != None:
            self.title.xml = etree.tostring(informe.find('report_title'))
            
        self.pages = []
        for pagina in informe.iterchildren('page'):
            page = ReportPage('')
            page.xml = etree.tostring(pagina)
            
            self.pages.append(page) 
    
    xml = property(getxml, setxml)
        
    def write(self, conector):
        print 'Report "%s"' % self.name
        
        self.title.write(conector)
        for page in self.pages:
            page.write(conector, self.params)