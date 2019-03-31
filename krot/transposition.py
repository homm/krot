from __future__ import print_function, absolute_import, unicode_literals

from collections import namedtuple


# Transposition methods
(FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90, ROTATE_180, ROTATE_270,
 TRANSPOSE, TRANSVERSE) = range(7)

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


def find_transposition_method(transposition):
    for method in transpose_table:
        if transpose_table[method] == transposition:
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


def combine_transposition_methods(first, second):
    return find_transposition_method(
        combine_transpositions(
            transpose_table[first], transpose_table[second]))
