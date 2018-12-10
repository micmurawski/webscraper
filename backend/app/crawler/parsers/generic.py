from urllib.parse import urljoin

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from .base import AbstractImageGenerator, AbstractParser


class GenericImageGenerator(AbstractImageGenerator):
    def _validate_image(self, pil_img):
        if pil_img.size[0] < 100:  # settings.CRAWLER_APP['DEFAULT_MIN_IMG_WIDTH']:
            return False
        if pil_img.size[1] < 100:  # settings.CRAWLER_APP['DEFAULT_MIN_IMG_HEIGHT']:
            return False

        return True


class GenericParser(AbstractParser):
    validator = URLValidator(schemes=('http', 'https'))
    image_generator_class = GenericImageGenerator
    img_ext = ('.gif', '.jpg', '.png', '.PNG', '.JPG', 'jpeg', 'svg')

    def __init__(self, payload, target_url):
        self.target_url = target_url
        super().__init__(payload=payload)

    def _url_validator(self, link):
        try:
            self.validator(link)
            return True
        except ValidationError as e:
            return False

    def _get_links(self):
        result = set()
        for link in self.soup.findAll(href=True):
            link = link.get('href')
            if link is not None:
                if self._url_validator(link):
                    if link.startswith(self.target_url):
                        result.add(link)
                elif self._url_validator(urljoin(self.target_url, link)):
                    result.add(urljoin(self.target_url, link))
        return result

    def _parse_link(self, link):
        if self._url_validator(link):
            return link
        elif link.startswith('//') and self._url_validator(urljoin('https:', link)):
            return urljoin('https:', link)
        elif self._url_validator(urljoin(self.target_url, link)):
            return urljoin(self.target_url, link)
        return None

    def _get_images_links(self):
        result = set()

        for link in self.soup.findAll(src=True):
            link = self._parse_link(link.get('src'))
            if link:
                result.add(link)

        for link in self.soup.findAll(href=True):
            link = link.get('href')
            if link.endswith(self.img_ext):
                link = self._parse_link(link)
                if link:
                    result.add(link)

        return result

    def _get_text(self):
        for script in self.soup(["script", "style"]):
            script.extract()
        return ' '.join(self.soup.get_text('\n').split())
