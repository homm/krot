from __future__ import print_function, absolute_import, unicode_literals

from PIL import Image

from .geometry import TranspositionMethod


class PillowAdapter(object):
    separable_resize = True
    
    _transpose_collation = {
        TranspositionMethod.DONT_TRANSPOSE: None,
        TranspositionMethod.FLIP_LEFT_RIGHT: Image.FLIP_LEFT_RIGHT,
        TranspositionMethod.FLIP_TOP_BOTTOM: Image.FLIP_TOP_BOTTOM,
        TranspositionMethod.ROTATE_90: Image.ROTATE_90,
        TranspositionMethod.ROTATE_180: Image.ROTATE_180,
        TranspositionMethod.ROTATE_270: Image.ROTATE_270,
        TranspositionMethod.TRANSPOSE: Image.TRANSPOSE,
        TranspositionMethod.TRANSVERSE: Image.TRANSVERSE,
    }

    @classmethod
    def get_image_stats(cls, image):
        if not isinstance(im, Image):
            raise TypeError("image should be an PIL.Image")
        return image.size, image.mode

    @classmethod
    def get_image_orientation(cls, image):
        return

    @classmethod
    def transpose_image(cls, image, method):
        method = cls._transpose_collation.get(method)
        if method is not None:
            image = image.transpose(method)
        return image
