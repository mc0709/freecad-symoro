#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import cos, sin
from numpy import matrix
from kinematics import Kinematics
from jacobians import serialKinematicJacobian as jacobian
from robots import table_rx90

kin = Kinematics(table_rx90)
kin.set_q([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
jnts = kin.joints

J1 = jacobian(jnts)

print(J1)

# From "Robots-manipulateurs de type série" - Wisama Khalil, Etienne Dombre, p.12.
# http://www.gdr-robotique.org/cours_de_robotique/?id=fd80a49ceaa004030c95cdacb020ec69.
# In French.
q0, q1, q2, q3, q4, q5 = kin.get_q()
c1 = cos(q0)
c2 = cos(q1)
c3 = cos(q2)
c4 = cos(q3)
c5 = cos(q4)
c6 = cos(q5)
s1 = sin(q0)
s2 = sin(q1)
s3 = sin(q2)
s4 = sin(q3)
s5 = sin(q4)
s6 = sin(q5)
c23 = cos(q1 + q2)
s23 = sin(q1 + q2)

print("\n");

# TODO: get D3 and RL4 from table_rx90
D3 = 300
RL4 = 400
J63_Khalil = matrix([[0, -RL4 + s3 * D3, -RL4, 0, 0, 0],
    [0, c3 * D3, 0, 0, 0, 0],
    [s23 * RL4 - c2 * D3, 0, 0, 0, 0, 0],
    [s23, 0, 0, 0, s4, -s5 * c4],
    [c23, 0, 0, 1, 0, c5],
    [0, 1, 1, 0, c4, s5 * s4]])
print (J63_Khalil)
print("\n");

D3 = table_rx90[2][7]
RL4 = table_rx90[3][9]
J63_Khalil = matrix([[0, -RL4 + s3 * D3, -RL4, 0, 0, 0],
    [0, c3 * D3, 0, 0, 0, 0],
    [s23 * RL4 - c2 * D3, 0, 0, 0, 0, 0],
    [s23, 0, 0, 0, s4, -s5 * c4],
    [c23, 0, 0, 1, 0, c5],
    [0, 1, 1, 0, c4, s5 * s4]])
print (J63_Khalil)
