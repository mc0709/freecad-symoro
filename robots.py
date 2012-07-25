revolute_joint_type = 0
prismatic_joint_type = 1
fixed_joint_type = 2
from math import pi

table1 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 1, revolute_joint_type,
        0, 0, 100, 0, 50, 0),
    (1, 0, 1, prismatic_joint_type,
        0, 0, 100, 1, 50, 0.5),
    (2, 0, 1, revolute_joint_type,
        0, 0, 0, 50, pi/2, 0),
    )

table_tree = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 1, revolute_joint_type,
        0, 0, 0, 0, 50, 0),
    (1, 0, 1, revolute_joint_type,
        0, 0, 1, 300, 0.5, 50),
    (2, 0, 1, revolute_joint_type,
        0, 0, 0, 200, pi/2, 0),
    (3, 0, 1, revolute_joint_type,
        0, 0, 0, 100, pi/2, 0),
    (2, 0, 1, revolute_joint_type,
        1, 0, 0, 300, -pi/2, 0),
    (5, 0, 1, revolute_joint_type,
        0, 0, 0, 100, pi/2, 0),
    )

table_rx90 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 1, revolute_joint_type,
        0, 0, 0, 0, 0, 0),
    (1, 0, 1, revolute_joint_type,
        0, 0, pi/2, 0, 0, 0),
    (2, 0, 1, revolute_joint_type,
        0, 0, 0, 300, 0, 0),
    (3, 0, 1, revolute_joint_type,
        0, 0, -pi/2, 0, 0, 400),
    (4, 0, 1, revolute_joint_type,
        0, 0, pi/2, 0, 0, 0),
    (5, 0, 1, revolute_joint_type,
        0, 0, -pi/2, 0, 0, 0)
        )

table_stanford = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 1, revolute_joint_type,
        0, 0, 0, 0, 0, 0),
    (1, 0, 1, revolute_joint_type,
        0, 0, -pi/2, 0, 0, 200),
    (2, 0, 1, prismatic_joint_type,
        0, 0, pi/2, 0, 0, 400),
    (3, 0, 1, revolute_joint_type,
        0, 0, 0, 0, 0, 0),
    (4, 0, 1, revolute_joint_type,
        0, 0, -pi/2, 0, 0, 0),
    (5, 0, 1, revolute_joint_type,
        0, 0, pi/2, 0, 0, 0)
    )

# SR400
d2 = 400
d3 = 800
d4 = 200
rl4 = 1000
d8 = 1000
table_sr400 = (
    # antecedant, sameas, mu, sigma,
    #   gamma, b, alpha, d, theta, r
    (0, 0, 1, revolute_joint_type,
        0, 0, 0, 0, 0, 0), # 1
    (1, 0, 1, revolute_joint_type,
        0, 0, -pi/2, d2, 0, 0), # 2
    (2, 0, 0, revolute_joint_type,
        0, 0, 0, d3, 0, 0), # 3
    (3, 0, 0, revolute_joint_type,
        0, 0, -pi/2, d4, 0, rl4), # 4
    (4, 0, 1, revolute_joint_type,
        0, 0, pi/2, 0, 0, 0), # 5
    (5, 0, 1, revolute_joint_type,
        0, 0, -pi/2, 0, 0, 0), # 6
    (1, 0, 1, revolute_joint_type,
        0, 0, -pi/2, d2, 0, 0), # 7
    (7, 0, 0, revolute_joint_type,
        0, 0, 0, d8, 0, 0), # 8
    (8, 0, 0, revolute_joint_type,
        0, 0, 0, d3, 0, 0), # 9
    (3, 9, 0, fixed_joint_type,
        pi/2, 0, 0, -d8, 0, 0), # 10
        )

