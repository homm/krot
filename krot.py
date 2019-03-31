from __future__ import print_function, absolute_import, unicode_literals

from collections import namedtuple

from PIL import Image


FLIP_LEFT_RIGHT = 0
FLIP_TOP_BOTTOM = 1
ROTATE_90 = 2
ROTATE_180 = 3
ROTATE_270 = 4
TRANSPOSE = 5
TRANSVERSE = 6

Transposition = namedtuple('Transposition',
                           'transpose flip_horizontal flip_vertical')
transpose_table = {
    None:            Transposition(False, False, False),
    FLIP_LEFT_RIGHT: Transposition(False, True, False),
    FLIP_TOP_BOTTOM: Transposition(False, False, True),
    ROTATE_90:       Transposition(True, False, True),
    ROTATE_180:      Transposition(False, True, True),
    ROTATE_270:      Transposition(True, True, False),
    TRANSPOSE:       Transposition(True, False, False),
    TRANSVERSE:      Transposition(True, True, True),
}


def combine_transpositions(first, second):
    # If the second operation transposes the image,
    # the meaning of the flip options of the first operation is flipped.
    if second.transpose:
        first = Transposition(first[0], first[2], first[1])
    return Transposition(
        first.transpose != second.transpose,
        first.flip_horizontal != second.flip_horizontal,
        first.flip_vertical != second.flip_vertical,
    )


def find_transposition_method(transposition):
    for method in transpose_table:
        if transpose_table[method] == transposition:
            return method
    raise ValueError(
        "A method for transposition {} is not found".format(transposition))


class DefaultPolicy(object):
    pass


class PillowAdapter(object):
    pass


class Krot(object):
    # Adjust some optional behavior
    policy = DefaultPolicy()

    # Adapter for the graphics library plus some performance stats
    adapter = PillowAdapter()

    def __init__(self, im, policy=None, adapter=None):
        if not isinstance(im, Image):
            raise TypeError('im should be an PIL.Image')
        self.im = im
        self.calls = []
        if policy is not None:
            self.policy = policy
        if adapter is not None:
            self.adapter = adapter

    def transpose(self, method):
        if method is not None:
            transposition = transpose_table[method]
            self.calls.append({'transpose': method})
