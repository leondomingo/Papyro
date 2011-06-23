# -*- coding: utf-8 -*-

import os.path
import sys
import datetime as dt
import reports
from reportlab.lib.units import mm

class ReportBase(object):
    """Base class for report generators (ReportPpf = PDF, ReportPlainText = Text, etc)"""
    
    def __init__(self, report, session):
        self.report = report
        self.session = session
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
        return dt.datetime.now().strftime(fmt)        
                    
    def apply_constants(self, text):
        """Looks for constants ocurrences in 'text' and returns the same text
        replacing those constants with its actual value"""
        
        # PAGE_NO
        text = text.replace('#PAGE_NO#', unicode(self.page_no))
        
        # DATE
        text = text.replace('#DATE#', dt.datetime.now().strftime('%d/%m/%Y'))
        
        # TIME
        text = text.replace('#TIME#', dt.datetime.now().strftime('%H:%M:%S'))
        
        # CR
        text = text.replace('#CR#', '\n')
        
        return text
    
    def apply_parameters(self, text):
        """Replaces param ocurrences in 'text' with their actual values and
        return the modified text"""
        for par in self.report.params.params:
            if par[1] != None:
                parameter = '#%s#' % par[0]
                text = self.replace_parameter(text, parameter, par[1])
            
        return text
    
    def apply_data(self, text, data):
        """Replaces field (of 'data') ocurrences in 'text' with their actual
        values and return the modified text"""
        if data != None:
            for k in data.keys():
                parameter = '#%s#' % unicode(k)
                text = self.replace_parameter(text, parameter, unicode(data[k]))
                
        return text
    
    def check_condition(self, cond, mdata=None, ddata=None):
        """Check the Python condition 'cond' and returns True or False.
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
        """Replace every piece of Python code inside {{ }} with the returning
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
            text_out = text_out.replace(script_name, unicode(script_result))
            
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
        """Returns wheter position 'i' in 'text' is inside a Python code block {{ }}"""         
        return i > text[i:].find('}}')
    
    def quote_string(self, value):
        return value.replace("'", "\\'")
    
    def is_optional(self, text, i):
        a = text.find('[', i)
        if a == -1: a = sys.maxint
        
        b = text.find(']', i)
        
        c = text.rfind(']', 0, i)
        d = text.rfind('[', 0, i)
         
        return c < d < i < b < a, d, b
    
    