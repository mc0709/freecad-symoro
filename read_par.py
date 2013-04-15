# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2013 Gael Ecorchard <galou_breizh@yahoo.fr>             *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__="FreeCAD Symoro+ Workbench - Read Symoro file (*.par)"
__author__ = "Gael Ecorchard <galou_breizh@yahoo.fr>"
__url__ = ["http://free-cad.sourceforge.net"]

import ply.lex as lex
import ply.yacc as yacc


def input_new(name):
    while True:
        try:
            v = float(raw_input('Value for "' + name + '": '))
        except ValueError:
            pass
        else:
            break
    return v


class ParLexer(object):
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lookup = {}

    keywords = [
            'NF', 'NL', 'NJ', 'Type',
            'Ant', 'Sigma', 'B', 'd', 'R',
            'gamma', 'Alpha', 'Mu', 'Theta',
            'XX', 'XY', 'XZ', 'YY', 'YZ', 'ZZ',
            'MX', 'MY', 'MZ', 'M',
            'IA', 'FV', 'FS', 'FX', 'FY', 'FZ',
            'CX', 'CY', 'CZ', 'QP', 'QDP',
            'W0', 'WP0', 'V0', 'VP0',
            'Z', 'G',
            ]

    tokens = [
            'COMMENT', 'NAME', 'KEYWORD', 'INTEGER', 'FLOAT', 'Pi',
            ]

    literals = ['=','+','-','*','/', '(', ')', '{', '}', ',']

    t_ignore = " \t\r"

    def t_COMMENT(self, t):
        r'\(\*.*'
        pass

    _keyword_pattern = '|'.join([r'\b' + k + r'\b' for k in keywords])
    from ply.lex import TOKEN
    @TOKEN(_keyword_pattern)
    def t_KEYWORD(self, t):
        return t

    def t_Pi(self, t):
        r'\bPi\b'
        from math import pi
        t.value = pi
        t.type = 'FLOAT'
        return t

    def t_FLOAT(self, t):
        r'[0-9.eE]+'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        try:
            t.value = self.lookup[t.value]
        except KeyError:
            val = input_new(t.value)
            self.lookup[t.value] = val
            t.value = val
        t.type = 'FLOAT'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


class ParParser:
    def __init__(self):
        self.lexer = ParLexer()
        self.tokens = self.lexer.tokens
        self.lookup = self.lexer.lookup
        #self.parser = yacc.yacc(module=self,write_tables=0,debug=False)
        self.parser = yacc.yacc(module=self)
        self.robot_definition = {}

    def parse(self, data):
        if data:
            return self.parser.parse(data, self.lexer.lexer, 0, 0, None)
        else:
            return []

    precedence = (
        ('left','+','-'),
        ('left','*','/'),
        ('right','UMINUS'),
        )

    def p_error(self, p):
        print 'Error!'
        print p
        print

    def p_expression_binop(self, p):
        """expression : expression '+' expression
                    | expression '-' expression
                    | expression '*' expression
                    | expression '/' expression"""
        if p[2] == '+'  :
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

    def p_expression_uminus(self, p):
        """expression : '-' expression %prec UMINUS"""
        p[0] = -p[2]

    def p_assignment(self, p):
        """assignment : keyword '=' '{' paramlist '}'"""
        self.robot_definition[p[0]] = p[3]

    def p_keyword(self, p):
        """keyword : """
        pass

    def p_paramlist(self, p):
        """paramlist : param ',' param
                       | param"""
        pass

if __name__ == '__main__':
    with open('RX90_geom.par', 'r') as f:
        rx90_geom = f.read()

    parlexer = ParLexer()
    parlexer.lexer.input(rx90_geom)
    for tok in parlexer.lexer:
        print(tok)

    #parser = ParParser()
    #parser.parse(rx90_geom)


