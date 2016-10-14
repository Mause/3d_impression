import numpy as np
from math import cos, sin, sqrt

ex_1, ey_1, ez_1 = 1 / sqrt(2), 0, 1 / sqrt(2)
ex_2, ey_2, ez_2 = -3 / sqrt(22), -2 / sqrt(22), 3 / sqrt(22)

# origin point
r_O = np.array((10, 10, 10))

vector_length = lambda a: sqrt(sum(t ** 2 for t in a))


def project(x, y, z):
    # target point
    r_P = np.array((x, y, z))

    # and your two coordinate axis in the plane are defined by
    e_1 = np.array((ex_1, ey_1, ez_1))
    e_2 = np.array((ex_2, ey_2, ez_2))

    assert 0 <= vector_length(e_1) <= 1
    assert 0 <= vector_length(e_2) <= 1

    return (
        e_1.dot(r_P - r_O),
        e_2.dot(r_P - r_O)
    )


def rotate(x, y, z, m):
    r_P = np.array((x, y, z))

    return m.dot(r_P)


def rotate_x(x, y, z, theta):
    return rotate(
        x, y, z,
        np.array([
            [cos(theta), -sin(theta), 0],
            [sin(theta), cos(theta), 0],
            [0, 0, 1]
        ])
    )


def rotate_y(x, y, z, theta):
    return rotate(
        x, y, z,
        np.array([
            [cos(theta), 0, sin(theta)],
            [0, 1, 0],
            [-sin(theta), 0, cos(theta)]
        ])
    )


def rotate_z(x, y, z, theta):
    return rotate(
        x, y, z,
        np.array([
            [1, 0, 0],
            [0, cos(theta), -sin(theta)],
            [0, sin(theta), cos(theta)]
        ])
    )
