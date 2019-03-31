from __future__ import print_function, absolute_import, unicode_literals

from collections import namedtuple

from PIL import Image


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


class DefaultPolicy(object):
    rotate_based_on_exif = True


class PillowAdapter(object):
    separable_resize = True
    transpose_collation = {
        FLIP_LEFT_RIGHT: Image.FLIP_LEFT_RIGHT,
        FLIP_TOP_BOTTOM: Image.FLIP_TOP_BOTTOM,
        ROTATE_90: Image.ROTATE_90,
        ROTATE_180: Image.ROTATE_180,
        ROTATE_270: Image.ROTATE_270,
        TRANSPOSE: Image.TRANSPOSE,
        TRANSVERSE: Image.TRANSVERSE,
    }

    @classmethod
    def get_image_stats(cls, image):
        if not isinstance(im, Image):
            raise TypeError('image should be an PIL.Image')
        return image.size, image.mode

    @classmethod
    def get_image_orientation(cls, image):
        return

    @classmethod
    def transpose_image(cls, image, method):
        if method:
            image = image.transpose(cls.transpose_collation.get(method))
        return image


class Krot(object):
    # Adjust some optional behavior
    policy = DefaultPolicy

    # Adapter for the graphics library plus some performance stats
    adapter = PillowAdapter

    def __init__(self, image, policy=None, adapter=None):
        if policy is not None:
            self.policy = policy
        if adapter is not None:
            self.adapter = adapter

        self.calls = []
        self.size, self.mode = self.adapter.get_image_stats(image)

        if self.policy.rotate_based_on_exif:
            self.transpose(self.adapter.get_image_orientation(image))

    def transpose(self, method):
        if method is not None:
            transposition = transpose_table[method]
            self.calls.append({'transpose': method})

    def resize(self, size, enlarge=True):
        pass
