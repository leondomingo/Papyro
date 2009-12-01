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
        
        ReportItem.setxml(self, valor)
        
    xml = property(getxml, setxml)
    
class GroupHeaderOptions(object):
    def __init__(self):
        self.print_on_new_page = False
        
    def getxml(self):
        valor = \
            '<options>\n' + \
            ('  <print_on_new_page/>\n' if self.print_on_new_page else '') + \
            '</options>\n'
                    
        return valor
    
    def setxml(self, valor):
        
        gh_options = etree.fromstring(valor)
        self.print_on_new_page = gh_options.find('print_on_new_page') != None
        
    xml = property(getxml, setxml)            
    
class GroupHeader(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.field = None
        self.options = GroupHeaderOptions()
        self.header = Header()
        self.footer_id = None
        
    def getxml(self):
        valor = \
            '<group_header>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            '  <field>' + (self.field or '') + '</field>\n' + \
            '  <footer_id>' + (self.footer_id or '') + '</footer_id>\n' + \
            self.options.xml + \
            ReportItem.getxml(self) + \
            self.header.xml + \
            '</group_header>\n'
            
        return valor
    
    def setxml(self, valor):
        gh = etree.fromstring(valor)
        
        self.id = gh.find('id').text or ''
        self.field = gh.find('field').text or ''
        if gh.find('footer_id') != None:
            self.footer_id = gh.find('footer_id').text
        self.options.xml = etree.tostring(gh.find('options'))
        self.header.xml = etree.tostring(gh.find('header'))
        
    xml = property(getxml, setxml)
    
class GroupFooter(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.footer = Body()
        
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
        self.footer.xml = etree.tostring(gf.find('body'))
        
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
    
class HeaderDetail(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.print_if_detail_is_empty = False
        self.body = Body()
        
    def getxml(self):
        value = \
            '<header>\n' + \
            ('  <print_if_detail_is_empty/>\n' if self.print_if_detail_is_empty else '') + \
            self.body.xml + \
            '</header>\n'
            
        return value
    
    def setxml(self, value):
        
        hd = etree.fromstring(value)
        
        self.id = hd.find('id').text or ''
        self.print_if_detail_is_empty = hd.find('print_if_detail_is_empty') != None
        
        self.body.xml = etree.tostring(hd.find('body'))
    
    xml = property(getxml, setxml)
    
class Detail(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)        
        self.id = id
        self.master_field = None
        self.table = Table()
        self.header = None
        self.body = Body()
        
    def getxml(self):
        valor = \
            '<detail>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            '  <master_field>' + (self.master_field or '') + '</master_field>\n' + \
            self.table.xml + \
            (self.header.xml if self.header != None else '') + \
            self.body.xml + \
            '</detail>\n'
            
        return valor
    
    def setxml(self, valor):
        detail = etree.fromstring(valor)
        
        self.id = detail.find('id').text or ''
        self.master_field = detail.find('master_field').text
        self.table.xml = etree.tostring(detail.find('table'))
        
        self.header = None
        h = detail.find('header')
        if h != None:
            self.header = HeaderDetail()
            self.header.xml = etree.tostring(h)
        
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

class Line(PrintableItem):
    def __init__(self, id=None):
        PrintableItem.__init__(self)        
        self.id = id or ''
        # en mm
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0        
        
    def getxml(self):
        valor = \
            '<line>\n' + \
            '  <id>' + self.id + '</id>\n' + \
            '  <x1>' + str(self.x1) + '</x1>\n' + \
            '  <y1>' + str(self.y1) + '</y1>\n' + \
            '  <x2>' + str(self.x2) + '</x2>\n' + \
            '  <y2>' + str(self.y2) + '</y2>\n' + \
            ReportItem.getxml(self) + \
            '</line>\n'
            
        return valor
    
    def setxml(self, valor):
        
        line = etree.fromstring(valor)
        
        self.id = line.find('id').text or ''
        self.x1 = int(line.find('x1').text)
        self.y1 = int(line.find('y1').text)
        self.x2 = int(line.find('x2').text)
        self.y2 = int(line.find('y2').text)
            
        ReportItem.setxml(self, valor)
            
    xml = property(getxml, setxml)
    
class Image(PrintableItem):
    def __init__(self, id=None):
        PrintableItem.__init__(self)        
        self.id = id or ''
        self.filename = None
        self.keep_aspect_ratio = False
        
    def getxml(self):
        valor = \
            '<image>\n' + \
            '  <id>' + self.id + '</id>\n' + \
            '  <filename>' + (self.filename or '') + '</filename>\n' + \
            ('  <keep_aspect_ratio/>\n' if self.keep_aspect_ratio else '') + \
            ReportItem.getxml(self) + \
            '</image>\n'
            
        return valor
    
    def setxml(self, valor):
        
        image = etree.fromstring(valor)
        
        self.id = image.find('id').text or ''
        self.filename = image.find('filename').text or ''
        self.keep_aspect_ratio = image.find('keep_aspect_ratio') != None
            
        ReportItem.setxml(self, valor)
            
    xml = property(getxml, setxml)    
    
class TextFile(PrintableItem):
    def __init__(self, id=None):
        PrintableItem.__init__(self)
        self.id = id
        self.name = None
        
    def getxml(self):
        value = \
            '<text_file>\n' + \
            '  <id>' + (self.id or '') + '</id>\n' + \
            '  <name>' + (self.name or '') + '</name>\n' + \
            '</text_file>'
            
        return value
    
    def setxml(self, value):
        
        tf = etree.fromstring(value)
        
        self.id = tf.find('id').text or ''
        self.name = tf.find('name').text or ''
        
    xml = property(getxml, setxml)
    
class SubParameters(object):
    def __init__(self):
        self.params = []
        
    def getxml(self):
        valor = '<params>\n'
        
        for par in self.params:
            valor += '<param value="%s">%s</param>\n' % (par[1] or '', par[0])
                            
        valor += '</params>\n'
        
        return valor
        
    def setxml(self, valor):        
        parametros = etree.fromstring(valor)        
        
        self.params = []
        for param in parametros.iterchildren('param'):
            self.params.append((param.text, param.attrib['value']))
            
    xml = property(getxml, setxml)
        
    
class SubReport(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id
        self.name = None
        self.params = SubParameters()
        
    def getxml(self):
        value = \
            '<subreport>\n' + \
            '  <id>' + self.id or '' '</id>\n' + \
            '  <name>' + self.name or '' + '</path>\n' + \
            self.params.xml + \
            '</subreport>\n'        
        
        return value
    
    def setxml(self, value):
        
        subinforme = etree.fromstring(value)
        
        self.id = subinforme.find('id').text or ''
        self.name = subinforme.find('name').text or ''
        self.params.xml = etree.tostring(subinforme.find('params')) 
    
    xml = property(getxml, setxml)

class Body(NotPrintableItem):
    def __init__(self):
        NotPrintableItem.__init__(self)        
        self.items = [] # lista de "ReportItem"
        self.split_on_new_page = False
        
    def getxmlitems(self):
        valor = ''
        for item in self.items:
            valor += item.xml
            
        return valor            
            
    def getxml(self):
        valor = \
            '<body>\n' + \
            ('  <split_on_new_page/>\n' if self.split_on_new_page else '') + \
            self.getxmlitems() + \
            '</body>\n'
            
        return valor
    
    def setxml(self, valor):        
        self.items = []
        bd = etree.fromstring(valor)
        
        self.split_on_new_page = bd.find('split_on_new_page') != None            
        
        for rep_item in bd.iterchildren():
            
            if rep_item.tag == 'text':
                txt = Text()
                self.items.append(txt)
                
                txt.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'text_file':
                txtf = TextFile()
                self.items.append(txtf)
                
                txtf.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'master':
                mas = Master()
                self.items.append(mas)
                
                mas.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'detail':
                det = Detail()
                self.items.append(det)
                
                det.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'crosstab':
                ct = CrossTab()
                self.items.append(ct)
                
                ct.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'image':
                im = Image()
                self.items.append(im)
                
                im.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'line':
                line = Line()
                self.items.append(line)
                
                line.xml = etree.tostring(rep_item)

                
    xml = property(getxml, setxml)
    
class CTHeader(Body):
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
    
class CTColumn(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.header = CTHeader()
        self.body = Body()
        self.width = None
        
    def getxml(self):
        value = \
            '<col>\n' + \
            self.header.xml + \
            self.body.xml + \
            '  <width>' + str(self.width or 0) + '</width>\n' + \
            '<\col>\n'
            
        return value
    
    def setxml(self, value):
        
        ctc = etree.fromstring(value)
        
        self.id = ctc.find('id').text or ''
        self.header.xml = etree.tostring(ctc.find('header'))
        self.body.xml = etree.tostring(ctc.find('body'))
        self.width = int(ctc.find('width').text or 0)        
    
    xml = property(getxml, setxml)
    
class CTColumns(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.columns = []
        
    def getcolumnsxml(self):
        value = ''
        for col in self.columns:
            value += col.xml
            
        return value
        
    def getxml(self):
        value = \
            '<columns>\n' + \
            self.getcolumnsxml() + \
            '</columns>\n'
        
        return value
    
    def setxml(self, value):
        self.columns = []
        ctc = etree.fromstring(value)
        
        self.id = ctc.find('id').text or ''
        
        for col in ctc.iterchildren('col'):
            new_col = CTColumn()
            new_col.xml = etree.tostring(col)
            self.columns.append(new_col)        
    
    xml = property(getxml, setxml)
    
class CTRowHeader(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.header = CTHeader()
        self.height = None
        
    def getxml(self):
        value = \
            '<rowheader>\n' + \
            self.header.xml + \
            '  <height>' + str(self.height or 0) + '</height>\n' + \
            '</rowheader>\n'
            
        return value
    
    def setxml(self, value):
        rh = etree.fromstring(value)
        
        self.id = rh.find('id').text or ''
        self.header.xml = etree.tostring(rh.find('header'))
        self.height = int(rh.find('height').text or 0)
    
    xml = property(getxml, setxml)
    
class CTRowHeaders(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.width = None
        self.rowheaders = []
        
    def getrowheadersxml(self):
        value = ''
        for rh in self.rowheaders:
            value += rh.xml
            
        return value
        
    def getxml(self):
        value = \
            '<rowheaders>\n' + \
            self.getrowheadersxml() + \
            '</rowheaders>\n'
            
        return value
    
    def setxml(self, value):
        self.rowheaders = []
        ctrh = etree.fromstring(value)
        
        self.id = ctrh.find('id').text or ''
        self.width = int(ctrh.find('width').text or 0)
        
        for rh in ctrh.iterchildren('rowheader'):
            new_rh = CTRowHeader()
            new_rh.xml = etree.tostring(rh)
            
            self.rowheaders.append(new_rh)
    
    xml = property(getxml, setxml)
        
        
class CrossTab(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.master = Master()
        self.detail = Detail()
        self.columns = CTColumns()
        self.rowheaders = CTRowHeaders()
        
    def getxml(self):
        value = \
            '<crosstab>\n' + \
            self.master.xml + \
            self.detail.xml + \
            self.columns.xml + \
            self.rowheaders.xml + \
            '<crosstab>\n'
            
        return value
    
    def setxml(self, value):
        ct = etree.fromstring(value)
        
        self.id = ct.find('id').text or ''
        self.master.xml = etree.tostring(ct.find('master'))
        self.detail.xml = etree.tostring(ct.find('detail'))
        self.columns.xml = etree.tostring(ct.find('columns'))
        self.rowheaders.xml = etree.tostring(ct.find('rowheaders'))
    
    xml = property(getxml, setxml)    
    
class Header(Body):
    def __init__(self):
        Body.__init__(self)
        
    def getxml(self):
        valor = \
            '<header>\n' + \
            ('  <split_on_new_page/>\n' if self.split_on_new_page else '') + \
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
        self.subreports = []
        self.switch_between_pages = False
        
        self.xml = xml
        
    def __repr__(self):
        return '"%s" (with %d pages)' % (self.name, len(self.pages))
        
    def getxmlpages(self):
        valor = ''
        for page in self.pages:
            valor += page.xml
            
        return valor
    
    def getxmlsubreports(self):
        valor = ''
        for sub in self.subreports:
            valor += sub.xml
            
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
            ('<switch_between_pages/>\n' if self.switch_between_pages else '') + \
            '  </configuration>\n' + \
            self.font.xml + \
            self.params.xml + \
            self.title.xml + \
            self.getxmlsubreports() + \
            self.getxmlpages() + \
            '</report>\n'
            
        return resultado                    
    
    def setxml(self, valor):
        report = etree.fromstring(valor)
        
        self.name = report.find('name').text
        
        if report.find('font') != None:
            self.font.xml = etree.tostring(report.find('font'))
         
        self.params.xml = etree.tostring(report.find('params'))
        
        paper = report.find('configuration').find('paper')
        self.paper_size = paper.find('size').text.upper()
        self.paper_orientation = paper.find('orientation').text.lower()
        
        self.switch_between_pages = report.find('configuration').find('switch_between_pages') != None
        
        margin = paper.find('margin')
        self.margin_left = float(margin.find('left').text or 0)
        self.margin_right = float(margin.find('right').text or 0)
        self.margin_top = float(margin.find('top').text or 0)
        self.margin_bottom = float(margin.find('bottom').text or 0)
        
        rt = report.find('report_title')
        if rt != None:
            self.title.xml = etree.tostring(report.find('report_title'))
            
        self.subreports = []
        for s in report.iterchildren('subreport'):
            subreport = SubReport()
            subreport.xml = etree.tostring(s)
            
            self.subreports.append(subreport)
            
        self.pages = []
        for p in report.iterchildren('page'):
            page = ReportPage('')
            page.xml = etree.tostring(p)
            
            self.pages.append(page) 
    
    xml = property(getxml, setxml)
    
    