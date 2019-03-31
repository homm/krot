from __future__ import print_function, absolute_import, unicode_literals

from enum import Enum
from functools import reduce
from collections import namedtuple


Transposition = namedtuple("Transposition",
                           "transpose flip_horizontal flip_vertical")


class TranspositionMethod(Enum):
    DONT_TRANSPOSE  = Transposition(False, False, False)
    FLIP_LEFT_RIGHT = Transposition(False, True, False)
    FLIP_TOP_BOTTOM = Transposition(False, False, True)
    ROTATE_90       = Transposition(True, False, True)
    ROTATE_180      = Transposition(False, True, True)
    ROTATE_270      = Transposition(True, True, False)
    TRANSPOSE       = Transposition(True, False, False)
    TRANSVERSE      = Transposition(True, True, True)


class ResizeMethod(Enum):
    (CONTAIN, CHANGE_RATIO, SCALE_CROP, ADD_PADDING) = range(4)


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


def reduce_transposition_methods(methods):
    return TranspositionMethod(reduce(
        combine_transpositions,
        map(lambda x: x.value, methods),
        TranspositionMethod.DONT_TRANSPOSE.value))
