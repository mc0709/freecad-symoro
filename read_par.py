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


def add_type(cls, t):
    """Add a token type"""
    from ply.lex import TOKEN

    @TOKEN(r'\b' + t + r'\b')
    def t_type(t):
        return t
    t_type.__name__ = 't_' + t
    setattr(cls, t_type.__name__, t_type)


class ParLex(object):
    def __init__(self):
        for k in self.keywords:
            add_type(self, k)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

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
            'COMMENT',
            'NAME','INTEGER', 'FLOAT', 'Pi',
            ] + keywords

    literals = ['=','+','-','*','/', '(', ')', '{', '}', ',']

    t_ignore = " \t\r"

    def t_COMMENT(self, t):
        r'\(\*.*'
        pass

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

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

