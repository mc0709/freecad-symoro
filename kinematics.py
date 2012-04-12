
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

__title__ = "FreeCAD Symoro+ Workbench - Kinematics"
__author__ = "Gael Ecorchard <galou_breizh@yahoo.fr>"
__url__ = ["http://free-cad.sourceforge.net"]

from joint import Joint
from chain import Chain

def table_ok(table):
    # Comparator function to order according to the antecedant index,
    # which is the first element in a joint description of the table
    # notation.
    cmp_antc = lambda j1, j2: cmp(j1[0], j2[0])
    sorted_table = sorted(table, cmp=cmp_antc)
    return (sorted_table == list(table))

class Kinematics():
    def __init__(self, table):
        self.table = table
        self.joints = self.get_joints_from_table(self.table)
        # List of actuated joints
        self.ajoints = self.get_ajoints()
        # List of passive joints
        self.pjoints = self.get_pjoints()
        # Actuated joints' variables
        self.q = self.get_q()
        # Passive joints' variables
        self.qp = self.get_qp()
        # Chains
        self.chains = Chain(self.joints)

    def get_joints_from_table(self, table):
        joints = []
        if not(table_ok):
            raise ValueError('Antecedants should be sorted in the table')
        for row in table:
            if (row[0] == 0):
                antc = None
            else:
                antc = joints[row[0] - 1]
            jnt = Joint(
                    antc=antc,
                    mu=row[1],
                    sigma=row[2],
                    gamma=row[3],
                    b=row[4],
                    alpha=row[5],
                    d=row[6],
                    theta=row[7],
                    r=row[8],
                    )
            joints.append(jnt)
        # TODO: add recursion detection for antecedants
        return joints

    def get_ajoints(self):
        """Return the list of active joints, always in the same order"""
        ajoints = []
        for jnt in self.joints:
            if (jnt.isactuated()):
                ajoints.append(jnt)
        return ajoints

    def get_pjoints(self):
        """Return the list of passive joints, always in the same order"""
        pjoints = []
        for jnt in self.joints:
            if (jnt.ispassive()):
                pjoints.append(jnt)
        return pjoints

    def get_q(self, index=None):
        if (index is None):
            return [jnt.q for jnt in self.ajoints]
        else:
            return self.ajoints[index].q

    def get_qp(self, index=None):
        if (index is None):
            return [jnt.q for jnt in self.pjoints]
        else:
            return self.pjoints[index].q

    def set_q(self, q, index=None):
        if (index is None):
            index = range(len(self.ajoints))
        try:
            self.ajoints[index].q = q
        except (AttributeError, TypeError):
            for i in index:
                self.ajoints[i].q = q[i]

    def set_qp(self, q, index=None):
        if (index is None):
            index = range(len(self.pjoints))
        try:
            self.pjoints[index].q = q
        except (AttributeError, TypeError):
            for i in index:
                self.pjoints[i].q = q[i]

