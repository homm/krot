from __future__ import print_function, absolute_import, unicode_literals

from .transposition import (FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM, ROTATE_90,
                            ROTATE_180, ROTATE_270, TRANSPOSE, TRANSVERSE)
try:
    from .pillow_adapter import PillowAdapter
except ImportError:
    # No default adapter in this case, should be defined in constructor
    PillowAdapter = None


class DefaultPolicy(object):
    rotate_based_on_exif = True


class Krot(object):
    # Adjust some optional behavior
    policy = DefaultPolicy

    # Adapter for the graphics library plus some performance stats
    adapter = PillowAdapter

    def __init__(self, image, policy=None, adapter=None):
        self.calls = []
        if policy is not None:
            self.policy = policy
        if adapter is not None:
            self.adapter = adapter
        assert self.adapter, ("You need to set custom adapter "
                              "or install Pillow to use the default adapter.")

        self.size, self.mode = self.adapter.get_image_stats(image)

        if self.policy.rotate_based_on_exif:
            self.transpose(self.adapter.get_image_orientation(image))

    def transpose(self, method):
        if method is not None:
            self.calls.append({'transpose': method})

    def resize(self, size, enlarge=True):
        pass
