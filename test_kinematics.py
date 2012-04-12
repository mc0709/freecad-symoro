#!/usr/bin/python
# -*- coding: utf-8 -*-

from kinematics import Kinematics

kin = Kinematics()

kin.set_q([1, 1, 1])

print(kin.ajoints[0].q)
