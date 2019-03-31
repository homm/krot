from __future__ import print_function, absolute_import, unicode_literals

from functools import reduce
import pytest
from PIL import Image

from .krot.transposition import transpose_table, combine_transpositions
from .krot import (FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90, ROTATE_180,
                   ROTATE_270, TRANSPOSE, TRANSVERSE)


@pytest.fixture(scope="module")
def transposition_image():
    im = Image.new('L', (10, 6), "black")
    im.load()[3, 1] = 255
    return im


@pytest.mark.parametrize("pipe,resulting_method", [
    ([None, None], None),
    ([None, FLIP_LEFT_RIGHT], FLIP_LEFT_RIGHT),
    ([None, FLIP_TOP_BOTTOM], FLIP_TOP_BOTTOM),
    ([None, ROTATE_90], ROTATE_90),
    ([None, ROTATE_180], ROTATE_180),
    ([None, ROTATE_270], ROTATE_270),
    ([None, TRANSPOSE], TRANSPOSE),
    ([None, TRANSVERSE], TRANSVERSE),

    ([FLIP_LEFT_RIGHT, None], FLIP_LEFT_RIGHT),
    ([FLIP_LEFT_RIGHT, FLIP_LEFT_RIGHT], None),
    ([FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM], ROTATE_180),
    ([FLIP_LEFT_RIGHT, ROTATE_90], TRANSPOSE),
    ([FLIP_LEFT_RIGHT, ROTATE_180], FLIP_TOP_BOTTOM),
    ([FLIP_LEFT_RIGHT, ROTATE_270], TRANSVERSE),
    ([FLIP_LEFT_RIGHT, TRANSPOSE], ROTATE_90),
    ([FLIP_LEFT_RIGHT, TRANSVERSE], ROTATE_270),

    ([FLIP_TOP_BOTTOM, None], FLIP_TOP_BOTTOM),
    ([FLIP_TOP_BOTTOM, FLIP_LEFT_RIGHT], ROTATE_180),
    ([FLIP_TOP_BOTTOM, FLIP_TOP_BOTTOM], None),
    ([FLIP_TOP_BOTTOM, ROTATE_90], TRANSVERSE),
    ([FLIP_TOP_BOTTOM, ROTATE_180], FLIP_LEFT_RIGHT),
    ([FLIP_TOP_BOTTOM, ROTATE_270], TRANSPOSE),
    ([FLIP_TOP_BOTTOM, TRANSPOSE], ROTATE_270),
    ([FLIP_TOP_BOTTOM, TRANSVERSE], ROTATE_90),

    ([ROTATE_90, None], ROTATE_90),
    ([ROTATE_90, FLIP_LEFT_RIGHT], TRANSVERSE),
    ([ROTATE_90, FLIP_TOP_BOTTOM], TRANSPOSE),
    ([ROTATE_90, ROTATE_90], ROTATE_180),
    ([ROTATE_90, ROTATE_180], ROTATE_270),
    ([ROTATE_90, ROTATE_270], None),
    ([ROTATE_90, TRANSPOSE], FLIP_LEFT_RIGHT),
    ([ROTATE_90, TRANSVERSE], FLIP_TOP_BOTTOM),


    ([ROTATE_180, None], ROTATE_180),
    ([ROTATE_180, FLIP_LEFT_RIGHT], FLIP_TOP_BOTTOM),
    ([ROTATE_180, FLIP_TOP_BOTTOM], FLIP_LEFT_RIGHT),
    ([ROTATE_180, ROTATE_90], ROTATE_270),
    ([ROTATE_180, ROTATE_180], None),
    ([ROTATE_180, ROTATE_270], ROTATE_90),
    ([ROTATE_180, TRANSPOSE], TRANSVERSE),
    ([ROTATE_180, TRANSVERSE], TRANSPOSE),

    ([ROTATE_270, None], ROTATE_270),
    ([ROTATE_270, FLIP_LEFT_RIGHT], TRANSPOSE),
    ([ROTATE_270, FLIP_TOP_BOTTOM], TRANSVERSE),
    ([ROTATE_270, ROTATE_90], None),
    ([ROTATE_270, ROTATE_180], ROTATE_90),
    ([ROTATE_270, ROTATE_270], ROTATE_180),
    ([ROTATE_270, TRANSPOSE], FLIP_TOP_BOTTOM),
    ([ROTATE_270, TRANSVERSE], FLIP_LEFT_RIGHT),

    ([TRANSPOSE, None], TRANSPOSE),
    ([TRANSPOSE, FLIP_LEFT_RIGHT], ROTATE_270),
    ([TRANSPOSE, FLIP_TOP_BOTTOM], ROTATE_90),
    ([TRANSPOSE, ROTATE_90], FLIP_TOP_BOTTOM),
    ([TRANSPOSE, ROTATE_180], TRANSVERSE),
    ([TRANSPOSE, ROTATE_270], FLIP_LEFT_RIGHT),
    ([TRANSPOSE, TRANSPOSE], None),
    ([TRANSPOSE, TRANSVERSE], ROTATE_180),

    ([TRANSVERSE, None], TRANSVERSE),
    ([TRANSVERSE, FLIP_LEFT_RIGHT], ROTATE_90),
    ([TRANSVERSE, FLIP_TOP_BOTTOM], ROTATE_270),
    ([TRANSVERSE, ROTATE_90], FLIP_LEFT_RIGHT),
    ([TRANSVERSE, ROTATE_180], TRANSPOSE),
    ([TRANSVERSE, ROTATE_270], FLIP_TOP_BOTTOM),
    ([TRANSVERSE, TRANSPOSE], ROTATE_180),
    ([TRANSVERSE, TRANSVERSE], None),

    ([FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90,
      ROTATE_180, ROTATE_270, TRANSPOSE, TRANSVERSE], ROTATE_180),
])
def test_transposition_combinations(transposition_image, pipe, resulting_method):
    # First, check that the test is correct and transformation pipe
    # is quivalent to the resulting_method.
    if resulting_method is None:
        resulting_image = transposition_image
    else:
        resulting_image = transposition_image.transpose(resulting_method)
    for method in pipe:
        if method is not None:
            transposition_image = transposition_image.transpose(method)
    assert transposition_image == resulting_image

    resulting_transposition = reduce(
        combine_transpositions,
        map(transpose_table.get, pipe),
        transpose_table[None])
    assert resulting_transposition == transpose_table[resulting_method]
