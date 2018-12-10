from abc import ABCMeta

import requests


class AbstractCrawler(metaclass=ABCMeta):

    def fetch_proxies(self):
        pass

    def fetch_data(self, target_url, proxy=None):
        try:
            if proxy is None:
                response = requests.get(url=target_url)
            else:
                response = requests.get(url=target_url, proxies={'http': proxy, 'https': proxy})
        except requests.exceptions.RequestException as e:
            return None, True
        return response.text, False


class GenericCrawler(AbstractCrawler):
    pass
