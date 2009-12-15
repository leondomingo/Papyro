# -*- coding: utf-8 -*-

from reports import Report
from lxml import etree
from datetime import datetime

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
        hbx_btn_inf = gtk.HBox(homogeneous=False)
        
        self.btn_exit = gtk.Button('Salir')
        self.btn_exit.connect('clicked', self.btn_exit_clicked)
        self.btn_exit.set_size_request(75, -1)
        hbx_btn_inf.pack_end(self.btn_exit, False)
        
        self.btn_add = gtk.Button('[1]')
        self.btn_add.connect('clicked', self.btn_add_clicked)
        hbx_btn_inf.pack_start(self.btn_add, False)

        self.btn_add2 = gtk.Button('[2]')
        self.btn_add2.connect('clicked', self.btn_add2_clicked)
        hbx_btn_inf.pack_start(self.btn_add2, False)
                
        self.vbx_botones = gtk.VBox(homogeneous=False)
        
        self.scw = gtk.ScrolledWindow()
        self.scw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.scw.add_with_viewport(self.vbx_botones)
        
        vbx_principal = gtk.VBox(homogeneous=False)
        vbx_principal.pack_start(self.scw)
        vbx_principal.pack_end(hbx_btn_inf, False)        
        
        self.window.add(vbx_principal)
        
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
        
    def btn_add_clicked(self, widget):
        nuevo_boton = gtk.Button(datetime.now().strftime('%H:%M:%S'))
        self.vbx_botones.pack_start(nuevo_boton, False, True, 1)
        nuevo_boton.show()
        
    def btn_add2_clicked(self, widget):
        nuevo_boton = gtk.Button(datetime.now().strftime('%H:%M:%S'))
        nuevo_boton.set_size_request(-1, 100)
        self.vbx_botones.pack_end(nuevo_boton, False, True, 1)
        nuevo_boton.show()
        
    def btn_exit_clicked(self, widget):
        self.window.destroy()
                    
if __name__ == '__main__':
    designer = Designer()
    designer.main()