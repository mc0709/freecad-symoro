
#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2012 Gael Ecorchard <galou_breizh@yahoo.fr>             *
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

__title__ = "FreeCAD Symoro+ Workbench - Joint"
__author__ = "Gael Ecorchard <galou_breizh@yahoo.fr>"
__url__ = ["http://free-cad.sourceforge.net"]

class Joint:
    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        antc: Joint or None
            Antecedent joint.
        mu: 0 or 1
            0 for passive joint, 1 for actuated joint.
        sigma: 0, 1, or 2
            0 for revolute joint, 1 for prismatic one and 2 for fixed.
        gamma, b, alpha, d, theta, r: float
            Parameters of modified Denavit-Hartenberg convention
            (Khalil-Kleinfinger convention).
        qinit: float, defaults to 0
            Start value used for the optimization.
        qmin, qmax: float, defaults to None (i.e. without limit)
            Joint limits.
        q: float, optional
            Current joint value.
        """
        self.antc = kwargs.get('antc')
        self.mu = kwargs.get('mu')
        self.sigma = kwargs.get('sigma')
        self.gamma = kwargs.get('gamma')
        self.b = kwargs.get('b')
        self.alpha = kwargs.get('alpha')
        self.d = kwargs.get('d')
        self.theta = kwargs.get('theta')
        self.r = kwargs.get('r')
        self.qmin = kwargs.get('qmin', None)
        self.qmax = kwargs.get('qmax', None)
        self.qinit = kwargs.get('qinit', 0)
        self.q = kwargs.get('q', 0)

    def ispassive(self):
        return (self.mu == 0)

    def isactuated(self):
        return (self.mu == 1)

    def isrevolute(self):
        return (self.sigma == 0)

    def isprismatic(self):
        return (self.sigma == 1)

    def isfixed(self):
        return (self.sigma == 2)

    def get_transform(self):
        """Return the transform from the antecedant joint"""
        if self.isrevolute():
            theta = self.theta + self.q
            r = self.r
        elif self.isprismatic():
            theta = self.theta
            r = self.r + self.q
        else:
            theta = self.theta
            r = self.r

        from math import cos, sin
        ct = cos(theta)
        st = sin(theta)
        ca = cos(self.alpha)
        sa = sin(self.alpha)
        cg = cos(self.gamma)
        sg = sin(self.gamma)

        T11 = ct * cg - sg * ca * st
        T12 = sg * ct + cg * ca * st
        T13 = sa * st
        T14 = 0
        T21 = -cg * st - sg * ca * ct
        T22 = -sg * st + cg * ca * ct
        T23 = sa * ct
        T24 = 0
        T31 = sa * sg
        T32 = -cg * sa
        T33 = ca
        T34 = 0
        T41 = self.d * cg + r * sg * sa
        T42 = self.d * sg - r * cg * sa
        T43 = r * ca + self.b
        T44 = 1
        T = [[T11, T21, T31, T41],
                [T12, T22, T32, T42],
                [T13, T23, T33, T43],
                [T14, T24, T34, T44]]
        return T

