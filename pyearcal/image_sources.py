import os
import fnmatch
import random
from collections import OrderedDict

class ImageDirectory(object):
    def __init__(self):  
        self.read_images()

    def __getitem__(self, index):
        return self.images[index]

    def __iter__(self):
        # yield from self.images.values()
        for image in self.images.values():
            yield image

class SortedImageDirectory(ImageDirectory):
    def __init__(self, dirname=".", extension=".jpg"):
        self.dirname = dirname
        self.extension = extension
        super(SortedImageDirectory, self).__init__()

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
        super(UnsortedImageDirectory, self).__init__()

    def read_images(self):
        self.images = OrderedDict()
        all_file_names = [ fn for fn in os.listdir(self.dirname) if fnmatch.fnmatch(fn, self.pattern) ]
        sampled_file_names = random.sample(all_file_names, 12)

        for index, name in enumerate(sampled_file_names):
            self.images[index + 1] = os.path.join(self.dirname, name)