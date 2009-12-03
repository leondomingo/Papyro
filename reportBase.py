# -*- coding: utf-8 -*-

import os.path
import sys
from datetime import datetime

class ReportBase(object):
    
    def __init__(self, report, conector):
        self.report = report
        self.conector = conector
        self.debug = False
        self.page_no = 0
        
        sys.path.append(self.report.path)
        
        # scripts
        for sc in self.report.scripts:
            global CODE
            CODE = __import__(os.path.splitext(sc.file)[0], globals(), locals())
            
    def get_date(self, format):
        return datetime.now().strftime(format)        
                    
    def apply_constants(self, text):
        
        # PAGE_NO
        text = text.replace('#PAGE_NO#', str(self.page_no))
        
        # DATE
        text = text.replace('#DATE#', datetime.now().strftime('%d/%m/%Y'))
        
        # TIME
        text = text.replace('#TIME#', datetime.now().strftime('%H:%M:%S'))
        
        # CR
        text = text.replace('#CR#', '\n')
        
        return text
    
    def apply_parameters(self, text):
        out = text
        for par in self.report.params.params:
            parameter = '#%s#' % par[0]
            out = out.replace(parameter, par[1])
            
        return out
    
    def apply_data(self, text, data):
        out = text
        if data != None:
            for k in data.keys():
                parameter = '#%s#' % str(k)
                out = out.replace(parameter, str(data[k]))
                
        return out
    
    def check_condition(self, cond, mdata=None, ddata=None):
        """Check the condition of the Python code 'cond' and returns True or False.
        If 'cond' is empty returns True."""
        if (cond or '') != '':
            # apply "constants"
            cond = self.apply_constants(cond)
            
            # apply "parameters"
            cond = self.apply_parameters(cond)
            
            # apply "masterdata"
            cond = self.apply_data(cond, mdata)
            
            # apply "detail data"
            cond = self.apply_data(cond, ddata)
            
            #print 'evaluating...%s' % cond
            return eval(cond)
        
        else:
            return True
    
    def execute_code(self, item):
        """Execute the code of the <code> 'item'"""
        if item.code != '':            
            # apply "constants"                        
            _code = self.apply_constants(item.code)
            
            # apply "parameters"
            _code = self.apply_parameters(_code)
            
            if self.debug: print 'executing...%s' % _code
            exec(_code)    
    
    def compile_text(self, text):
        """Replace every piece of Python code inside {{...}} with the returning
        value of its execution"""
        
        text_out = ''
        scripts = []
        n = 0
        j = -2
        i = text.find('{{')
        while i != -1:
            text_out += text[(j+2):i]
            j = text[(i+2):].find('}}')
            
            if j != -1:
                j += (i + 2)
                scripts.append(text[(i+2):j])
                text_out += '#SCRIPT%d#' % (n + 1)
                
                i = text[j+2:].find('{{') + j + 2
            else:
                j = i - 1
                i = -1                
            
            n += 1
        
        i = len(text)
        text_out += text[(j+2):i]
        
        n = 0
        for sc in scripts:
            script_result = eval(sc)
            script_name = '#SCRIPT%d#' % (n + 1)
            text_out = text_out.replace(script_name, str(script_result))
            
            n += 1
            
        return text_out
    
#    def inside_code(self, text, parameter):
#        
#        inside = False
#        i = text.find('{{')
#        while i != -1:
#            p = text[i+2:].find('parameter')
#                
#        
#        return inside
#    
#    def quote_string(self, value):
#        
#        return "'%s'" % value.replace("'", "\\'")