import requests
import random
import os
from .image_sources import SortedImageDirectory
from bs4 import BeautifulSoup

TEMP_DIR = ".flickr-download"
EXTENSION = ".jpg"


class FlickrDownloader(SortedImageDirectory):
    """Image source that downloads random pictures from Flickr.

    Based on the article
        http://blog.art21.org/2011/09/20/how-to-use-python-to-create-a-simple-flickr-photo-glitcher
    """

    def download_images(self, number: int = 12) -> None:
        response = requests.get(
            "https://api.flickr.com/services/feeds/photos_public.gne?tags="
            + self.keyword
            + "&lang=en-us&format=rss_200"
        )
        soup = BeautifulSoup(response.content, "lxml")

        image_list = []
        for image in soup.findAll("media:content"):
            image_url = dict(image.attrs)["url"]
            image_list.append(image_url)
        image_list = random.sample(image_list, number)

        if not os.path.isdir(TEMP_DIR):
            os.makedirs(TEMP_DIR)
        for index, image in enumerate(image_list):
            response = requests.get(image)
            with open(
                os.path.join(TEMP_DIR, f"{index + 1}{EXTENSION}"), "wb"
            ) as output_file:
                output_file.write(response.content)
            response.close()
            print(f"Downloaded picture {index + 1} of {number} from flickr.")

    def __init__(self, keyword: str = "python"):
        """
        :param keyword: a keyword to look for on flickr.
        """
        self.keyword = keyword
        self.dirname = TEMP_DIR
        self.extension = EXTENSION
        self.download_images()
        self.read_images()
