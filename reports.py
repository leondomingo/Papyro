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
        self.size = int(fuente.find('size').text)
        self.color = fuente.find('color').text
        
        self.style[0] = fuente.find('bold') != None
        self.style[1] = fuente.find('italic') != None
        self.style[2] = fuente.find('underline') != None
        self.style[3] = fuente.find('strike') != None
        
    xml = property(getxml, setxml)
    
class Parameters(object):
    def __init__(self):
        self.parameters = []
        
    def getxml(self):
        valor = '<params>\n'
        
        for par in self.parameters:
            valor += '<param name="%s">%s</param>\n' % (par[0], par[1])
                            
        valor += '</params>\n'
        
    def setxml(self, valor):
        print valor
        parametros = etree.tostring(valor)
        
        self.parameters = []
        for param in parametros.iter('param'):
            self.parameters.append((param.find('name').text, param.find('value').text))
            
    xml = property(getxml, setxml)

class ReportItem(object):
    def __init__(self):
        self.left = None
        self.top = None
        self.height = None
        self.width = None
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
            self.left = int(pos.find('left').text)
            self.top = int(pos.find('top').text)
                
        size = item.find('size')
        if size != None:
            self.height = int(size.find('height').text)
            self.width = int(size.find('width').text)
            
        if item.find('font'):
            self.font.xml = etree.tostring(item.find('font'))
        
    xml = property(getxml, setxml)   
        
    
class PrintableItem(ReportItem):
    def __init__(self):
        ReportItem.__init__(self)        

class NotPrintableItem(ReportItem):
    def __init__(self):
        ReportItem.__init__(self)   
        
class PageHeader(NotPrintableItem):
    def __init__(self, id):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()
        
    def write(self):
        print 'PageHeader "%s"' % self.id
        ReportItem.write(self)
        self.body.write()
    
class PageFooter(NotPrintableItem):
    def __init__(self, id):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()
    
    def write(self):
        print 'PageFooter "%d"' % self.id
        ReportItem.write(self)
        self.body.write() 
    
class GroupHeader(NotPrintableItem):
    def __init__(self, id):
        NotPrintable.__init__(self)
        self.id = id
        self.body = Body()
        
    def write(self):
        print 'GroupHeader "%s"' % self.id
        ReportItem.write(self)
        self.body.write()
    
class GroupFooter(NotPrintableItem):
    def __init__(self):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()   

    def write(self):
        print 'GroupFooter "%s"' % self.id
        ReportItem.write(self)
        self.body.write()
        
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
        for fld in tabla.find('fields').iter('field'):
            self.fields.append(fld.text)
        
    xml = property(getxml, setxml)
    
class Detail(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)        
        self.id = id
        self.master_field = None
        self.table = Table()
        self.body = Body()
        
    def write(self, conector, master_data):
#        print 'Detail "%s" (%s)' % (self.id, self.master_field)
#        ReportItem.write(self)

        # tratar SQL
        master_dict = {}
        master_dict[self.master_field] = master_data[self.master_field]
        sql = self.table.query % master_dict        
        
        for detail_data in conector.conexion.execute(sql):
            #print 'detail_data =', detail_data
            if detail_data != None:
                self.body.write(conector, master_data, detail_data)
        
    def getxml(self):
        valor = \
            '<detail>\n' + \
            '  <master_field>' + (self.master_field or '') + '</master_field>\n' + \
            self.table.xml + \
            self.body.xml + \
            '</detail>\n'
            
        return valor
    
    def setxml(self, valor):
        detail = etree.fromstring(valor)
        
        self.master_field = detail.find('master_field').text
        self.table.xml = etree.tostring(detail.find('table'))
        self.body.xml = etree.tostring(detail.find('body'))
    
    xml = property(getxml, setxml)
    
class Master(NotPrintableItem):
    def __init__(self, id=None):
        NotPrintableItem.__init__(self)
        self.id = id or ''
        self.table = Table()
        self.body = Body()
        self.details = []
        
    def write(self, conector):
#        print 'Master "%s"' % self.id
        ReportItem.write(self)
        
        for master_data in conector.conexion.execute(self.table.query):
            self.body.write(conector, master_data)
            
            for detalle in self.details:
                detalle.write(conector, master_data)
                
    def getxmldetails(self):
        valor = ''
        for dt in self.details:
            valor += dt.xml
            
        return valor

    def getxml(self):
        valor = \
            '<master>\n' + \
            self.table.xml + \
            self.body.xml + \
            self.getxmldetails() + \
            '</master>\n'
        return valor
    
    def setxml(self, valor):
        master = etree.fromstring(valor)
        
        self.table.xml = etree.tostring(master.find('table'))
        self.body.xml = etree.tostring(master.find('body'))
        
        self.details = []
        for detalle in master.iter('detail'):
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
        return '"%s" = "%s" (%s)' % (self.id, self.value or '', self.field or '')
        
    def write(self, master=None, detail=None):
#        print 'Text "%s" = "%s" (%s)' % (self.id, self.value or '', self.field or '')
#        print ReportItem.write(self)

        out = self.value
        if master != None:
            for k in master.keys():
                k2 = '#' + str(k) + '#'
                out = out.replace(k2, str(master[k]))
                
        if detail != None:
            for k in detail.keys():
                k2 = '#' + str(k) + '#'
                out = out.replace(k2, str(detail[k]))            
                
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
        
        self.id = texto.find('id').text
        self.value = texto.find('value').text        
            
        ReportItem.setxml(self, valor)
            
    xml = property(getxml, setxml) 
        
class Label(PrintableItem):
    def __init__(self, id=None):
        PrintableItem.__init__(self)
        
        self.id = id or ''
        self.caption = None
        
    def __repr__(self):
        return '"%s" = "%s"' % (self.id, self.caption or '')
        
    def write(self, master=None, detail=None):
#        print 'Label "%s" = "%s"' % (self.id, self.caption)
#        ReportItem.write(self)
        
        out = self.caption
        if master != None:
            for k in master.keys():
                k2 = '#' + str(k) + '#'
                out = out.replace(k2, str(master[k]))
                
        if detail != None:
            for k in detail.keys():
                k2 = '#' + str(k) + '#'
                out = out.replace(k2, str(detail[k]))
                
        print out        
        
    def getxml(self):
        valor = \
            '<label>\n' + \
            '  <id>' + self.id + '</id>\n' + \
            '  <caption>' + (self.caption or '') + '</caption>\n' + \
            ReportItem.getxml(self) + \
            '</label>\n'
            
        return valor
    
    def setxml(self, valor):        
        etiqueta = etree.fromstring(valor)
        self.id = etiqueta.find('id').text
        self.caption = etiqueta.find('caption').text
        
        ReportItem.setxml(self, valor)
        
    xml = property(getxml, setxml)

class Body(NotPrintableItem):
    def __init__(self):
        NotPrintableItem.__init__(self)        
        self.items = [] # lista de "ReportItem"
        
    def write(self, conector, master=None, detail=None):
        
        for item in self.items:
            if isinstance(item, Master):
                #print self, item.id
                item.write(conector)
            else:
                item.write(master, detail)
            
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
        
        for rep_item in cuerpo.iter():
            
            if rep_item.tag == 'label':
                lbl = Label()
                self.items.append(lbl)
                
                lbl.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'text':
                txt = Text()
                self.items.append(txt)
                
                txt.xml = etree.tostring(rep_item)
                
            elif rep_item.tag == 'master':
                mas = Master()
                self.items.append(mas)
                
                mas.xml = etree.tostring(rep_item)
                
    xml = property(getxml, setxml)
            

class ReportPage(object):
    def __init__(self, id, num=None):
#        self.page_header = PageHeader()
#        self.page_footer = PageFooter()
        self.body = Body()
        self.num = num or 1
        self.id = id
        
    def __repr__(self):
        return '"%s" (page=%d)' % (self.id, self.num)
        
    def write(self, conector):
#        print 'ReportPage "%s" (p=%d)' % (self.id, self.num)        
        self.body.write(conector)
        
    def getxml(self):
        valor = \
            '<page>\n' + \
            '  <id>' + self.id + '</id>\n' + \
            '  <number>' + str(self.num) + '</number>\n' + \
            self.body.xml + \
            '</page>\n'
            
        return valor
    
    def setxml(self, valor):        
        pagina = etree.fromstring(valor)
        
        self.id = pagina.find('id').text
        self.num = int(pagina.find('number').text)
        
        body = pagina.find('body')
        if body != None:
            self.body.xml = etree.tostring(body) 
        
    xml = property(getxml, setxml)
        
class ReportTitle(NotPrintableItem):
    def __init__(self, id):
        NotPrintableItem.__init__(self)
        self.id = id
        self.body = Body()
        
    def __repr__(self):
        return '"%s"' % self.id
        
    def write(self, conector):
        print '"%s"' % self.id
#        ReportItem.write(self)
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
        
        self.id = titulo.find('id').text
        
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
        self.parameters = Parameters()
        
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
            self.parameters.xml + \
            self.title.xml + \
            self.getxmlpages() + \
            '</report>\n'
            
        return resultado                    
    
    def setxml(self, valor):
        informe = etree.fromstring(valor)
        
        self.name = informe.find('name').text
         
        self.parameters.xml = etree.tostring(informe.find('params'))
        
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
        for pagina in informe.iter('page'):
            page = ReportPage('')
            page.xml = etree.tostring(pagina)
            
            self.pages.append(page) 
    
    xml = property(getxml, setxml)
        
    def write(self, conector):
        print 'Report "%s"' % self.name
        self.title.write(conector)
        for page in self.pages:
            page.write(conector)

if __name__ == '__main__':
    
    import cStringIO
    from unidadescompartidas import conexion
    
    f = file('./report0.xml', 'r')
    try:    
        informe = Report(xml=f.read())
        
        rep = etree.fromstring(informe.xml)
        print etree.tostring(rep, pretty_print=True)
        
        conector = conexion()        
        informe.write(conector)
    finally:
        f.close()