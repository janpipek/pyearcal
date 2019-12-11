import abc
import os
import fnmatch
import random
from typing import Dict
from collections import OrderedDict


class ImageDirectory(abc.ABC):
    def __getitem__(self, index: int) -> str:
        return self.images[index]

    images: Dict[int, str]

    def __iter__(self):
        # yield from self.images.values()
        for image in self.images.values():
            yield image


class SortedImageDirectory(ImageDirectory):
    def __init__(self, dirname=".", extension=".jpg"):
        self.dirname = dirname
        self.extension = extension
        self.read_images()

    def read_images(self):
        self.images = OrderedDict()
        for index in range(1, 13):
            path = os.path.join(self.dirname, str(index) + self.extension)
            if os.path.exists(path):
                self.images[index] = path
            else:
                raise Exception("File does not exist: " + path)


class UnsortedImageDirectory(ImageDirectory):
    def __init__(self, dirname=".", pattern="*.jpg"):
        self.dirname = dirname
        self.pattern = pattern
        self.read_images()

    def read_images(self):
        self.images = OrderedDict()
        all_file_names = [
            fn for fn in os.listdir(self.dirname) if fnmatch.fnmatch(fn, self.pattern)
        ]
        sampled_file_names = random.sample(all_file_names, 12)

        for index, name in enumerate(sampled_file_names):
            self.images[index + 1] = os.path.join(self.dirname, name)
