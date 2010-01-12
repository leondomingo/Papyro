# -*- coding: utf-8 -*-

#from reports import Report
from datetime import datetime 

import pygtk
pygtk.require('2.0')
import gtk #, gobject, pango

TIPO_PAGE = 'page'

BTN_PAGEHEADER = 'page_header'
BTN_PAGEFOOTER = 'page_footer'
BTN_MASTER = 'master'
BTN_DETAIL = 'detail'
BTN_GROUPHEADER = 'group_header'
BTN_GROUPFOOTER = 'group_footer'

BANDAS_DISPONIBLES = {
                      TIPO_PAGE:
                      {
                       BTN_PAGEHEADER: True,
                       BTN_PAGEFOOTER: True,
                       BTN_MASTER: False,
                       BTN_DETAIL: False,
                       BTN_GROUPHEADER: False,
                       BTN_GROUPFOOTER: False
                      },
                     }

class Designer(object):
    
    def __init__(self):        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Papyro designer')
        self.window.set_position(gtk.WIN_POS_CENTER)
        #self.window.set_default_size(500, 500)
        self.window.resize(1000, 600)
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
        
        # bandas
        vbx_bandas = gtk.VBox(homogeneous=False)
        vbx_bandas.set_size_request(100, -1)
        
        btn_color = gtk.ColorButton()
        vbx_bandas.pack_end(btn_color, False, False, 2)       
        
        # page header        
        self.btn_pageheader = gtk.Button('Page Header')
        vbx_bandas.pack_start(self.btn_pageheader, False, False, 2)
        
        # page footer
        self.btn_pagefooter = gtk.Button('Page Footer')
        vbx_bandas.pack_start(self.btn_pagefooter, False, False, 2)
        
        # master
        self.btn_master = gtk.Button('Master')
        vbx_bandas.pack_start(self.btn_master, False, False, 2)
        
        # group header
        self.btn_gheader = gtk.Button('Group Header')
        vbx_bandas.pack_start(self.btn_gheader, False, False, 2)
        
        # group footer
        self.btn_gfooter = gtk.Button('Group Footer')
        vbx_bandas.pack_start(self.btn_gfooter, False, False, 2)
        
        # detail
        self.btn_detail = gtk.Button('Detail')
        vbx_bandas.pack_start(self.btn_detail, False, False, 2)
        
        # datos de la banda
        vbx_datosbanda = gtk.VBox(homogeneous=False)
        vbx_datosbanda.set_size_request(250, -1)
        
        hbx_idbanda = gtk.HBox(homogeneous=False)
        edt_idbanda = gtk.Entry()
        edt_idbanda.set_text('(id)')
        
        lbl_tipobanda = gtk.Label('<b>Page Header</b>')
        lbl_tipobanda.set_use_markup(True)                

        hbx_idbanda.pack_start(lbl_tipobanda, False, False, 3)
        hbx_idbanda.pack_start(edt_idbanda, True)
        
        vbx_datosbanda.pack_start(hbx_idbanda, False, False)        
        
        hbx_principal = gtk.HBox(homogeneous=False)
        hbx_principal.pack_start(vbx_bandas, False)
        hbx_principal.pack_start(self.scw)
        hbx_principal.pack_start(vbx_datosbanda, False)        
        
        vbx_principal = gtk.VBox(homogeneous=False)
        vbx_principal.pack_start(hbx_principal)        
        vbx_principal.pack_end(hbx_btn_inf, False)        
        
        self.window.add(vbx_principal)
        
        self.window.show_all()
        
        self.update_bandas_disponibles('body')
        
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
        
    def update_bandas_disponibles(self, tipo):
        
        if BANDAS_DISPONIBLES.has_key(tipo):
            self.btn_pageheader.set_sensitive(BANDAS_DISPONIBLES[tipo][BTN_PAGEHEADER])
            self.btn_pagefooter.set_sensitive(BANDAS_DISPONIBLES[tipo][BTN_PAGEFOOTER])
            self.btn_master.set_sensitive(BANDAS_DISPONIBLES[tipo][BTN_MASTER])
            self.btn_detail.set_sensitive(BANDAS_DISPONIBLES[tipo][BTN_DETAIL])
            self.btn_gheader.set_sensitive(BANDAS_DISPONIBLES[tipo][BTN_GROUPHEADER])
            self.btn_gfooter.set_sensitive(BANDAS_DISPONIBLES[tipo][BTN_GROUPFOOTER])
            
        else:                                          
            self.btn_pageheader.set_sensitive(True)
            self.btn_pagefooter.set_sensitive(True)
            self.btn_master.set_sensitive(True)
            self.btn_detail.set_sensitive(True)
            self.btn_gheader.set_sensitive(True)
            self.btn_gfooter.set_sensitive(True)
                    
if __name__ == '__main__':
    designer = Designer()
    designer.main()