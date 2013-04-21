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
            #v = float(raw_input('Value for "' + name + '": '))
            v = 0
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
            'COMMENT', 'KEYWORD', 'NUMBER', 'Pi', 'NEWLINE', 'NAME',
            ]

    literals = ['=','+','-','*','/', '(', ')', '{', '}', ',']

    #states = (
    #    ('paramlist', 'inclusive'),
    #)

    t_ignore = " \t\r"

    #def t_begin_paramlist(self, t):
    #    r'\{'
    #    t.lexer.push_state('paramlist')

    #def t_end_paramlist(self, t):
    #    r'\}'
    #    t.lexer.pop_state()

    def t_COMMENT(self, t):
        r'\(\*.*'
        pass

    _keyword_pattern = '|'.join([r'\b' + k + r'\b' for k in keywords])
    from ply.lex import TOKEN
    @TOKEN(_keyword_pattern)
    def t_KEYWORD(self, t):
        return t

    # Within braces keywords are treated as names, though this is not supported
    # by Symoro+.
    #@TOKEN(_keyword_pattern)
    #def t_paramlist_KEYWORD(self, t):
    #    return self.t_NAME(t)

    def t_Pi(self, t):
        r'\bPi\b'
        from math import pi
        t.value = pi
        t.type = 'NUMBER'
        return t

    def t_NUMBER(self, t):
        r'[0-9.eE]+'
        t.value = float(t.value)
        return t

    def t_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        try:
            t.value = self.lookup[t.value]
        except KeyError:
            val = input_new(t.value)
            self.lookup[t.value] = val
            t.value = val
        t.type = 'NUMBER'
        return t

    def t_NEWLINE(self, t):
        r'[\n]+'
        t.lexer.lineno += t.value.count("\n")
        return t

    #def t_paramlist_NEWLINE(self, t):
    #    r'[\n]+'
    #    t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


class ParParser(object):
    def __init__(self):
        self.lexer = ParLexer()
        self.tokens = self.lexer.tokens
        self.lookup = self.lexer.lookup
        #self.parser = yacc.yacc(module=self,write_tables=0,debug=False)
        self.parser = yacc.yacc(module=self, debug=1)
        self.robot_definition = {}

    def parse(self, data):
        if data:
            #return self.parser.parse(data, self.lexer.lexer, 0, 0, None)
            return self.parser.parse(data, self.lexer.lexer,
                    False, 0, None)
        else:
            return []

    precedence = (
        ('left', ','),
        ('left','+','-'),
        ('left','*','/'),
        ('right','UMINUS'),
        )

    def p_input(self, p):
        """input :
                | input line"""
        pass

    def p_line(self, p):
        """line : assignment NEWLINE
                | NEWLINE"""
        pass

    def p_assignment(self, p):
        """assignment : KEYWORD '=' param
                      | KEYWORD '=' '{' NEWLINE paramlist '}'"""
        print('in p_assignment, p = {}'.format(list(p)))
        if len(p) == 4:
            # assignment : KEYWORD '=' param
            self.robot_definition[p[1]] = p[3]
        else:
            # assignment : KEYWORD '=' '{' NEWLINE paramlist '}'
            self.robot_definition[p[1]] = p[5]

    def p_paramlist(self, p):
        """paramlist : paramlist ',' param
                       | param"""
        print('in p_paramlist, p = {}'.format(list(p)))
        if len(p) == 4:
            # paramlist : paramlist ',' param
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_param(self, p):
        """param : expression
                 | '(' expression ')'"""
        print('in p_param, p = {}'.format(list(p)))
        index = 1 if len(p) == 2 else 2
        p[0] = p[index]

    def p_expression_binop(self, p):
        """expression : expression '+' expression
                    | expression '-' expression
                    | expression '*' expression
                    | expression '/' expression"""
        print('in p_expression_binop, p = {}'.format(list(p)))
        if p[2] == '+'  :
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[1] == '(' and p[3] == ')':
            p[0] = p[2]

    def p_expression_uminus(self, p):
        """expression : '-' expression %prec UMINUS"""
        print('in p_expression_uminus, p = {}'.format(list(p)))
        p[0] = -p[2]

    def p_expression_term(self, p):
        """expression : NAME
                    | NUMBER
                    | Pi"""
        print('in p_expression_term, p = {}'.format(list(p)))
        p[0] = p[1]

    def p_error(self, p):
        print 'Error!'
        print p
        print

if __name__ == '__main__':
    with open('RX90_geom.par', 'r') as f:
        rx90_geom = f.read()

    #parlexer = ParLexer()
    #parlexer.lexer.input(rx90_geom)
    #for tok in parlexer.lexer:
    #    print(tok)

    parser = ParParser()
    parser.parse(rx90_geom)
    print parser.robot_definition


