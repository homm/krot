from __future__ import print_function, absolute_import, unicode_literals

from PIL import Image

from .transposition import (FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90,
                            ROTATE_180, ROTATE_270, TRANSPOSE, TRANSVERSE)


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
