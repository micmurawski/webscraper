import base64
from abc import ABCMeta
from io import BytesIO

import requests
from bs4 import BeautifulSoup

from .utils import get_pil_image_from_response_content


class AbstractImageGenerator(metaclass=ABCMeta):
    def __init__(self, image_links_array):
        self.image_links_array = image_links_array

    def __iter__(self):
        return self

    def _validate_image(self, pil_img):
        raise NotImplemented

    def __next__(self):
        while self.image_links_array:
            next_url = self.image_links_array.pop()
            try:
                response = requests.get(next_url)
                try:
                    img = get_pil_image_from_response_content(content=response.content)
                    img.filename = next_url.rsplit('/', 1)[1]
                    if self._validate_image(img):
                        buffered = BytesIO()
                        img.save(buffered, format=img.format)
                        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        return img.filename, img_str
                except OSError as e:
                    pass
            except requests.exceptions.ConnectionError as e:
                pass

        if len(self.image_links_array) == 0:
            raise StopIteration


class AbstractParser(metaclass=ABCMeta):
    soup = None
    image_generator_class = NotImplemented
    image_generator = None
    img_ext = NotImplemented

    def __init__(self, payload):
        self.soup = BeautifulSoup(payload, "lxml")

    def _get_links(self):
        raise NotImplemented

    def _get_text(self):
        raise NotImplemented

    def _get_images_links(self):
        raise NotImplemented

    def url_validator(self, link):
        raise NotImplemented

    @property
    def links(self):
        return self._get_links()

    @property
    def text(self):
        return self._get_text()

    @property
    def images_links(self):
        return self._get_images_links()

    @property
    def images(self):
        if self.image_generator is None:
            self.image_generator = self.image_generator_class(self._get_images_links())
        return self.image_generator

    @property
    def next_image(self):
        if self.image_generator is None:
            self.image_generator = self.image_generator_class(self._get_images_links())
            return next(self.image_generator)
        return next(self.image_generator)
