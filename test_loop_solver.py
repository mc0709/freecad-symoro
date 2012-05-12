#!/usr/bin/python
# -*- coding: utf-8 -*-

from robots import table_sr400
from kinematics import Kinematics
from loop_solver import LoopSolver
kin = Kinematics(table_sr400)
jnts = kin.joints
ls = LoopSolver(jnts, jnts[0], jnts[8])

assert(ls.get_end_joints() == [jnts[8], jnts[9]])

from loop_solver import frame_diff
from numpy import matrix, identity, allclose
T0 = matrix(identity(4))
T1 = matrix(identity(4))
assert(allclose(frame_diff(T0, T1), 0))

J = ls.get_cjoint_jac()

# ls.solve()

