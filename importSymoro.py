
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

__title__ = "FreeCAD Symoro+ Workbench - import file"
__author__ = "Gael Ecorchard <galou_breizh@yahoo.fr>"
__url__ = ["http://free-cad.sourceforge.net"]

import FreeCAD
from FreeCAD import Base, Part
from kinematics import Kinematics

revolute_joint_type = 0
prismatic_joint_type = 1
fixed_joint_type = 2
from math import pi
table1 = (
    # antecedant, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 1, revolute_joint_type,
        0, 0, 100, 0, 50, 0),
    (1, 1, prismatic_joint_type,
        0, 0, 100, 1, 50, 0.5),
    (2, 1, revolute_joint_type,
        0, 0, 0, 50, pi/2, 0),
    )

# Parameters for the graphical representation
d_rev = 20
l_rev = 200
d_prism = 20
l_prism = 200
d_body = 5

def Ttomatrix(T):
    l = T[0] + T[1] + T[2] + T[3]
    return Base.Matrix(*l)

class Mechanism():
    def __init__(self, feature):
        self.kinematics = Kinematics(table1)
        self.qstr = ['q{0}'.format(i+1) for i in range(len(self.kinematics.ajoints))]
        add_rev = lambda s: feature.addProperty("App::PropertyAngle",
                s, "Joint Values", s)
        add_prism = lambda s: feature.addProperty("App::PropertyDistance",
                s, "Joint Values", s)
        for jnt, qstr in zip(self.kinematics.ajoints, self.qstr):
            if (jnt.isrevolute()):
                add_rev(qstr)
            elif (jnt.isprismatic()):
                add_prism(qstr)
        feature.Proxy = self

    def onChanged(self, feature, prop):
        if prop.startswith('q'):
            self.set_joint_values(feature)
            self.createShape(feature)

    def execute(self, feature):
        self.createShape(feature)

    def set_joint_values(self, feature):
        q = [feature.getPropertyByName(s) for s in self.qstr]
        self.kinematics.set_q(q)
        for jnt in self.kinematics.joints:
            if (jnt.isrevolute()):
                from math import pi
                jnt.q *= pi / 180

    def createShape(self, feature):
        comp = Part.Compound([])
        Pjminus1 = Base.Vector(0, 0, 0)
        m = Base.Matrix()
        for jnt in self.kinematics.joints:
            m *= Ttomatrix(jnt.get_transform())
            Pj = Base.Vector(m.A14, m.A24, m.A34)
            v = Pj - Pjminus1
            if (v.Length > 0):
                body_shape = Part.makeCylinder(d_body, v.Length, Pjminus1, v)
                #body_obj = doc.addObject('Part::Feature', 'Body{0}'.format(i))
                #body_obj.Shape = body_shape
                comp.add(body_shape)
            if (jnt.isrevolute()):
                joint_shape = Part.makeCylinder(d_rev, l_rev, Base.Vector(0, 0, -l_rev/2))
            elif (jnt.isprismatic()):
                joint_shape = Part.makeBox(d_prism, d_prism, l_prism, Base.Vector(0, 0, -l_prism/2))
            if not(jnt.isfixed()):
                joint_shape.Matrix = m
                #joint_obj = doc.addObject('Part::Feature', 'Joint{0}'.format(i))
                #joint_obj.Shape = joint_shape
                comp.add(joint_shape)
            Pjminus1 = Pj
        feature.Shape = comp

doc = FreeCAD.activeDocument()
if doc == None:
    doc = FreeCAD.newDocument()
mechanism = doc.addObject("Part::FeaturePython","Mechanism")
mechanism.Label = "Mechanism"
Mechanism(mechanism)
mechanism.ViewObject.Proxy = 0
doc.recompute()
import FreeCADGui as Gui
Gui.SendMsgToActiveView("ViewFit")

