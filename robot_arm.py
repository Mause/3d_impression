from main import block, connect_points, Point, rad
import numpy as np
from projection import *
from functools import reduce

# first, build
# then, rotate
# then, translate

from math import sin

concat = lambda *bits: reduce(lambda a, b: np.append(a, b, axis=0), bits)

ARM_THICKNESS = 1.0
ARM_LENGTH = 10.0


def jaw(step):
    return block(1.5, .5, 1.5, to_origin=True)


def claw(step):
    lines = block(.75, 3, 1.5, to_origin=True)

    one = jaw(step) + Point(1.5 * sin(step), .75, 0)

    return concat(
        lines,
        one,
        apply_to_points(
            lambda r_P: rotate_y(r_P, rad(180)),
            one
        )
    )


def second_section(step):
    lines = block(ARM_LENGTH, ARM_THICKNESS, ARM_THICKNESS, to_origin=True)

    lines = concat(
        lines,
        claw(step) + Point(0, ARM_LENGTH, 0),
    )

    degrees = 90
    if step > 10:
        degrees += step * 2

    return apply_to_points(
        lambda r_P: rotate_x(r_P, rad(degrees)),
        lines
    )


def first_section(step):
    lines = block(ARM_LENGTH, ARM_THICKNESS, ARM_THICKNESS, to_origin=True)

    lines = concat(
        lines,
        second_section(step) + Point(0, ARM_LENGTH, 0),
    )

    return apply_to_points(
        lambda r_P: rotate_y(
            rotate_x(
                r_P,
                rad(step * 3)
            ),
            rad(step * 5)
        ),
        lines
    )


def apply_to_points(func, arr):
    return np.apply_along_axis(
        func,
        2,
        arr
    )


def rotate_upright(r_P, by):
    return rotate_x(rotate_z(r_P, by), by)


def base(step):
    width = 4
    height = 4
    depth = 4

    lines = concat(
        block(height, width, depth),
        first_section(step) + Point(width / 2, height, depth / 2),
    )
    assert lines.shape[1:] == (2, 3)

    lines -= Point(width / 2, 10, depth / 2)

    return apply_to_points(
        lambda r_P: rotate_upright(r_P, rad(-13)),
        lines
    )


def robot_arm(step):
    yield from base(step)
