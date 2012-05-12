#!/usr/bin/python
# -*- coding: utf-8 -*-

from kinematics import Kinematics
from robots import table1
from robots import table_sr400

kin = Kinematics(table1)
kin.set_q([1, 1, 1])
assert(kin.ajoints[0].q == 1)

from kinematics import get_looproot
kin = Kinematics(table_sr400)
jnts = kin.joints
assert(get_looproot(jnts, jnts[9]) == jnts[0])

from kinematics import get_loops
kin = Kinematics(table_sr400)
jnts = kin.joints
assert(get_loops(jnts) == [(jnts[0], jnts[8])])

