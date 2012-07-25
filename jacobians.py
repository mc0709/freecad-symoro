
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

__title__ = "FreeCAD Symoro+ Workbench - jabobians"
__author__ = "Gael Ecorchard <galou_breizh@yahoo.fr>"
__url__ = ["http://free-cad.sourceforge.net"]

import numpy as np

def serialKinematicJacobian(joints):
    """Return the kinematic Jacobian of a serial chain

    Passive joints are considered to be as if they were actuated. The end
    joint is the last joint in the list and the base joint is its farest
    antecedent.
    """
    from chain import Chain
    from chain import get_subchain_to

    chain = Chain(get_subchain_to(joint=joints[-1], joints=joints))

    # We need the position of last joint frame in the base joints frame
    from serialmechanism import end_transform
    T = end_transform(chain.joints)
    Pend = T[0:3, 3]

    jacobian = np.matrix(np.zeros((6, len(chain.get_mjoints()))))
    T = np.matrix(np.identity(4))
    k = 0
    for jnt in chain.joints:
        T *= jnt.T
        if jnt.isrevolute():
            P = T[0:3, 3]
            DP = Pend - P
            jacobian_trans = np.cross(P, DP, axis=0)
            jacobian_rot = P
        if jnt.isprismatic():
            jacobian_trans = T[0:3, 3]
            jacobian_rot = np.zeros(3)
        if not(jnt.isfixed()):
            jacobian[:3, k] = jacobian_trans
            jacobian[3:, k] = jacobian_rot
            k += 1
    # If the last joint is fixed, apply the Jacobian transposition
    if (joints[-1].isfixed()):
        P = jnt.T[0:3, 3]
        jac_transposition = np.matrix(np.identity(6))
        jac_transposition[3, 1] = -P[2]
        jac_transposition[3, 2] = P[1]
        jac_transposition[4, 0] = P[2]
        jac_transposition[4, 2] = -P[0]
        jac_transposition[5, 0] = -P[1]
        jac_transposition[5, 1] = P[0]

        jacobian = jac_transposition * jacobian
    return jacobian

def serialKinematicJacobianPassive(joints):
    """Return the kinematic Jacobian of a serial chain

    Passive joints are considered to be as if they were actuated. Actuated
    joints are considered to be fixed. The end joint is the last joint in
    the list and the base joint is its farest antecedent.
    """
    # Jacobians with passive and actuated joints
    jac_all = serialKinematicJacobian(joints)
    # List of indexes of passive joints
    p_indexes = [i for i, jnt in enumerate(joints) if jnt.ispassive()]
    return jac_all[:, p_indexes]

