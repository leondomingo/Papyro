# -*- coding: utf-8 -*-

import os.path
import sys
from datetime import datetime
import reports
from reportlab.lib.units import mm

class ReportBase(object):
    
    def __init__(self, report, conector):
        self.report = report
        self.conector = conector
        self.debug = False
        self.page_no = 0
        self.cur_item = None
        self.cur_y = 0
        
        sys.path.append(self.report.path)
        
        # scripts
        for sc in self.report.scripts:
            global CODE
            CODE = __import__(os.path.splitext(sc.file)[0], globals(), locals())
            
    def get_date(self, fmt):
        return datetime.now().strftime(fmt)        
                    
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
        for par in self.report.params.params:
            parameter = '#%s#' % par[0]
            text = self.replace_parameter(text, parameter, par[1])
            
        return text
    
    def apply_data(self, text, data):
        if data != None:
            for k in data.keys():
                parameter = '#%s#' % str(k)
                text = self.replace_parameter(text, parameter, str(data[k]))
                
        return text
    
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
    
    def execute_code(self, item, y, mdata=None, ddata=None):
        """Execute the code of the <code> 'item'"""
        min_y = y
        if item.code != '':
            # apply "constants"                        
            _code = self.apply_constants(item.code)
            
            # apply "parameters"
            _code = self.apply_parameters(_code)
            
            # applyt "data" (master, detail)
            _code = self.apply_data(_code, mdata)
            _code = self.apply_data(_code, ddata)
                        
            if self.debug: print 'executing...%s' % _code
            exec(_code)
        
        return min_y    
    
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
    
    def replace_parameter(self, text, parameter, value):
        """Replaces every occurrence in 'text' of 'parameter' with 'value'"""
        
        if text.find('{{') != -1 and text.find('}}') != -1:        
            r = text.partition(parameter)
            while r[1] != '':
                if self.inside_code(text, len(r[0])):
                    text = r[0] + self.quote_string(value) + r[2]
                    
                else:
                    text = r[0] + value + r[2]
                    
                r = text.partition(parameter)
        
        else:
            text = text.replace(parameter, value)            
        
        return text
    
    def inside_code(self, text, i):
        
        a = text[i:].find('}}')
        
        return i > a   
    
    def quote_string(self, value):
        return value.replace("'", "\\'")