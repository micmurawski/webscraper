from django.apps import AppConfig


class CrawlerConfig(AppConfig):
    name = 'app.crawler'

    def ready(self):
        import app.crawler.signals  # flake8:noqa
