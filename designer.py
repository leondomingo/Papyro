# -*- coding: utf-8 -*-

from reports import Report
from lxml import etree

import pygtk
pygtk.require('2.0')
import gtk, gobject

class Designer(object):
    
    def __init__(self):        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Papyro designer')
        #self.window.set_default_size(500, 500)
        self.window.resize(800, 600)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect('delete-event', self.window_delete_event)
        self.window.connect('destroy', self.window_destroy)
        
        # botones inferiores
        hbox_btn_inf = gtk.HBox(homogeneous=False)
        
        self.btn_exit = gtk.Button('Salir')
        self.btn_exit.connect('clicked', self.btn_exit_clicked)
        self.btn_exit.set_size_request(75, -1)
        hbox_btn_inf.pack_end(self.btn_exit, False)
        
        vbox_1 = gtk.VBox(homogeneous=False)
        vbox_1.pack_end(hbox_btn_inf, False)
        
        informe = Report(reportfile='./report1/report1.xml')
        
        # tree
        hbox = gtk.HBox(homogeneous=False)
        vbox_1.pack_start(hbox, False)
        
        self.ts_report = gtk.TreeStore(str)        
        self.tv_report = gtk.TreeView(self.ts_report)
        
        self.col_report = gtk.TreeViewColumn('Report')
        
        self.tv_report.append_column(self.col_report)
        
        self.cell_report = gtk.CellRendererText()
        self.col_report.pack_start(self.cell_report, True)
        self.col_report.add_attribute(self.cell_report, 'text', 0)
        
        self.add_data(informe.xml, None)    
        
        hbox.pack_start(self.tv_report)
        
        self.window.add(vbox_1)
        
        self.window.show_all()
        
    def main(self):
        gtk.main()
        
    def window_destroy(self, widget):
        gtk.main_quit()
        return False
    
    def window_delete_event(self, widget, event, data=None):
        
        dlg = gtk.MessageDialog(self.window, gtk.DIALOG_DESTROY_WITH_PARENT, \
                                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, \
                                '¿Seguro que desea salir de la aplicación?')
        
        dlg.set_title('Papyro designer')
        
        r = dlg.run()
        dlg.destroy()
            
        if r == gtk.RESPONSE_YES:
            gtk.main_quit()
            return False
        else:
            return True
        
    def btn_exit_clicked(self, widget):
        self.window.destroy()
        
    def add_data(self, xml, parent):
        
        if xml != None:        
            node = etree.fromstring(xml)
            
            if node.text != None:
                text = '%s= %s' % (node.tag, node.text)
            else:
                text = node.tag
            
            tree_node = self.ts_report.append(parent, [text])
            
            for ch in node.iterchildren():            
                self.add_data(etree.tostring(ch), tree_node)
            
if __name__ == '__main__':
    designer = Designer()
    designer.main()