from __future__ import print_function, absolute_import, unicode_literals

from functools import reduce
from collections import namedtuple


_consts = (
    # Transposition methods
    "FLIP_LEFT_RIGHT FLIP_TOP_BOTTOM ROTATE_90 ROTATE_180 ROTATE_270 "
    "TRANSPOSE TRANSVERSE "
    # Resize methods
    "CONTAIN CHANGE_RATIO SCALE_CROP ADD_PADDING "
).strip().split(" ")

__all__ = _consts + (
    "Transposition combine_transpositions transpose_methods_table "
    "combine_transposition_methods "
).strip().split(" ")

for _index, _name in enumerate(_consts):
    globals()[_name] = _index
del _index, _name, _consts


Transposition = namedtuple("Transposition",
                           "transpose flip_horizontal flip_vertical")

transpose_methods_table = {
    None:            Transposition(False, False, False),
    FLIP_LEFT_RIGHT: Transposition(False, True, False),
    FLIP_TOP_BOTTOM: Transposition(False, False, True),
    ROTATE_90:       Transposition(True, False, True),
    ROTATE_180:      Transposition(False, True, True),
    ROTATE_270:      Transposition(True, True, False),
    TRANSPOSE:       Transposition(True, False, False),
    TRANSVERSE:      Transposition(True, True, True),
}


def find_transposition_method(transposition):
    for method in transpose_methods_table:
        if transpose_methods_table[method] == transposition:
            return method
    raise ValueError(
        "A method for transposition {} is not found".format(transposition))


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


def combine_transposition_methods(methods):
    return find_transposition_method(reduce(
        combine_transpositions,
        map(transpose_methods_table.get, methods),
        transpose_methods_table[None]))
