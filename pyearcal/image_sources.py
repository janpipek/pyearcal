import abc
import os
import fnmatch
import random
from typing import Dict, Iterable
from collections import OrderedDict


class ImageSource(abc.ABC):
    """Base class for image sources."""

    def __getitem__(self, index: int) -> str:
        return self.images[index]

    images: Dict[int, str]

    def __iter__(self) -> Iterable[str]:
        for image in self.images.values():
            yield image


class SortedImageDirectory(ImageSource):
    """Image source that returns images in sorted order.

    The image files have to be named in the format "1.jpg", "2.jpg", etc.
    (or whatever the extension is).
    """

    def __init__(self, dirname=".", extension=".jpg"):
        self.dirname = dirname
        self.extension = extension
        self.read_images()

    def read_images(self) -> None:
        self.images = OrderedDict()
        for index in range(1, 13):
            path = os.path.join(self.dirname, str(index) + self.extension)
            if os.path.exists(path):
                self.images[index] = path
            else:
                raise Exception(f"File does not exist: {path}")


class UnsortedImageDirectory(ImageSource):
    """Image directory with images in random order."""

    def __init__(self, dirname=".", pattern="*.jpg"):
        self.dirname = dirname
        self.pattern = pattern
        self.read_images()

    def read_images(self):
        self.images = OrderedDict()
        all_file_names = [
            fn for fn in os.listdir(self.dirname) if fnmatch.fnmatch(fn, self.pattern)
        ]
        if len(all_file_names) < 12:
            raise ValueError(f"Not enough images in directory: {len(all_file_names)}")
        sampled_file_names = random.sample(all_file_names, 12)

        for index, name in enumerate(sampled_file_names):
            self.images[index + 1] = os.path.join(self.dirname, name)
