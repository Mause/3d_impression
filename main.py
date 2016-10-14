# heights -> blocks
# blocks -> image
from pathlib import Path
from math import pi

import yaml
import numpy as np
import cairocffi as cairo

from projection import project, rotate_y

rad = lambda t: t * pi / 180

Point = lambda x, y, z: np.array([x, y, z])
Point.zero = Point(0, 0, 0)
Line = lambda start, end: np.array([start, end])
Line.as_ = lambda single: Line(single, single)
Line.zero = Line.as_(Point.zero)


class Rectangle:

    def __init__(self, p1, p2, p3, p4):
        self.lines = [
            Line(p1, p2),
            Line(p2, p3),
            Line(p3, p4),
            Line(p4, p1)
        ]
        self.points = (p1, p2, p3, p4)

    def __iter__(self):
        return iter(self.lines)

    def __add__(self, other):
        return Rectangle(
            *[
                s + o
                for s, o in zip(self.points, other.points)
            ]
        )

    def as_(single):
        return Rectangle(single, single, single, single)


def block(height, width, depth):
    bottom = Rectangle(
        Point(0, 0, 0),
        Point(0, 0, depth),
        Point(width, 0, depth),
        Point(width, 0, 0)
    )

    height_added = Point(0, height, 0)
    top = bottom + Rectangle.as_(height_added)

    yield from bottom
    yield from top
    yield from (
        Line(tp, bp)
        for tp, bp in zip(bottom.points, top.points)
    )


def get_lines(blocks):
    WIDTH, DEPTH = 1, 1
    for x, row in enumerate(blocks):
        for z, y in enumerate(row):
            x *= WIDTH
            z *= DEPTH
            y *= 10

            for line in block(y, WIDTH, DEPTH):
                yield line + Line.as_(Point(x, 0, z))


def rgb_to_decimal(*rgb):
    if len(rgb) == 1:
        rgb, = rgb
    return (comp / 256 for comp in rgb)


def render(blocks, theta):
    lines = get_lines(blocks)

    im = cairo.ImageSurface(
        cairo.FORMAT_RGB24,
        720, 720
    )
    draw = cairo.Context(im)
    draw.set_antialias(cairo.ANTIALIAS_BEST)

    with draw:
        draw.set_source_rgb(*rgb_to_decimal(256, 200, 256))
        draw.paint()

    for parts in lines:
        parts *= 25

        parts = np.array([
            project(*rotate_y(*part, theta=theta))
            for part in parts
        ])

        parts[:, 0] += im.get_width() / 2  # bump the x
        parts[:, 1] += im.get_height() / 2  # bump the y
        start, end = parts

        with draw:
            draw.move_to(*start)
            draw.line_to(*end)
            draw.stroke()

    return im


def save(im):
    number = max(
        (
            int(t.stem)
            for t in Path('.').glob('pngs/*.png')
        ),
        default=0
    ) + 1

    with open('pngs/{:03d}.png'.format(number), 'wb') as fh:
        im.write_to_png(fh)


def main():
    with open('blocks.yaml') as fh:
        blocks = yaml.load(fh)

    for theta in range(361):
        save(render(blocks, rad(theta)))


if __name__ == '__main__':
    main()
