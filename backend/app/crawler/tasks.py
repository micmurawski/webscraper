from django.conf import settings

from app.media.models import Image
from app.media.strategies import get_upload_strategy
from settings.celery import app

from .crawlers import CRAWLER_MAPPING
from .models.page import Page
from .models.task import Task
from .parsers import PARSER_MAPPING


def check_if_url_exists_within_task(task, target_url):
    if task.pages.all().filter(task_id=task.id, target_url=target_url):
        return True
    return False


def process_images(task, parser, task_node):
    for filename, image in parser.images:
        strategy_class = get_upload_strategy(task.images_storage)
        strategy = strategy_class(filename=filename, image=image,
                                  max_size=settings.CRAWLER_APP['DEFAULT_MAX_IMG_SIZE'])
        strategy.execute()
        image_url = strategy.url
        image, created = Image.objects.get_or_create(filename=filename, url=image_url, storage=0)
        task_node.images.add(image)
        task_node.save()


def process_page(task, parser_class, crawler, link):
    payload, error = crawler.fetch_data(link)
    parser = parser_class(payload=payload, target_url=task.target_url)
    if not error:
        page = Page.objects.create(task_id=task.id, target_url=link, error=error, done=True)

        if task.parse_text:
            page.text = parser.text
            page.save()

        if task.parse_images:
            process_images(task, parser, page)

        return parser.links

    Page.objects.create(task_id=task.id, target_url=link, error=error, done=True)
    return set()


@app.task(ignore_result=True)
def execute_task(_task_id):
    task = Task.objects.get(id=_task_id)

    crawler_class = CRAWLER_MAPPING[task.crawler]
    crawler = crawler_class()

    parser_class = PARSER_MAPPING[task.parser]
    if not task.pages.all():
        links = process_page(task, parser_class, crawler, task.target_url)
        for i in range(0, task.depth - 1):
            new_links = set()
            for link in links:
                if not check_if_url_exists_within_task(task, link):
                    result = process_page(task, parser_class, crawler, link)
                    new_links = new_links | result
            links = new_links
    else:
        task.error = True
    task.done = True
    task.save()
