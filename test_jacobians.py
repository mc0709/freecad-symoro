#!/usr/bin/python
# -*- coding: utf-8 -*-

from kinematics import Kinematics
from jacobians import serialKinematicJacobian as jacobian
from robots import table_rx90

kin = Kinematics(table_rx90)
kin.set_q([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
jnts = kin.joints

J1 = jacobian(jnts)

print(J1)
