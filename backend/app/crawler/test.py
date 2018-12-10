import os
import unittest
from urllib.parse import urljoin

from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse

from httmock import HTTMock, urlmatch
from rest_framework.test import APIClient

from .models.page import Page
from .models.task import Task
from .tasks import execute_task


@urlmatch(netloc=r'(.*\.)?testserver\.com$')
def request_mock(url, request):
    if settings.MEDIA_URL in url.path:
        file_path = url.path.rsplit('/', 1)[1]
        file = open(os.path.join(settings.MEDIA_ROOT, file_path), 'rb')

        return {'status_code': 200, 'content': file.read()}
    response = APIClient().get(url.path)
    return {'status_code': response.status_code, 'content': response.content}


class CrawlerTestCase(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://testserver.com'
        self.tasks_list_url = reverse('crawler:tasks-list')
        self.tasks_detail_route = 'crawler:tasks-detail'
        self.client = APIClient()
        self.test_page_urls = [
            reverse('crawler:home'),
            reverse('crawler:page_1'),
            reverse('crawler:page_2'),
            reverse('crawler:page_3'),
            reverse('crawler:page_4')
        ]
        self.task1 = Task.objects.create(depth=7, target_url=urljoin(self.base_url, self.test_page_urls[0]))
        self.task2 = Task.objects.create(depth=7, target_url=urljoin(self.base_url, self.test_page_urls[0]),
                                         task_type='1')
        self.task3 = Task.objects.create(depth=7, target_url=urljoin(self.base_url, self.test_page_urls[0]),
                                         task_type='0')

    @override_settings(DEBUG=True, CELERY_TASK_ALWAYS_EAGER=True)
    def test_celery_task(self):
        with HTTMock(request_mock):
            execute_task(_task_id=self.task1.id)
            page_1 = Page.objects.get(target_url=urljoin(self.base_url, self.test_page_urls[0]))
            self.assertEqual(page_1.images.all().count(), 2)
            page_4 = Page.objects.get(target_url=urljoin(self.base_url, self.test_page_urls[4]))
            self.assertEqual(page_4.images.all().count(), 1)
            self.assertEqual(self.task1.pages.all().count(), 5)

    def test_task_list_api_view(self):
        response = self.client.get(self.tasks_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['done'], True)
        self.assertEqual(response.data['results'][0]['pages_count'], 5)

    def test_task_detail_api_view(self):
        response = self.client.get(reverse(self.tasks_detail_route, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['done'], True)
        self.assertEqual(response.data['pages_count'], 5)

    @override_settings(DEBUG=True, CELERY_TASK_ALWAYS_EAGER=True)
    def test_task_create(self):
        response = self.client.post(self.tasks_list_url,
                                    data={'target_url': urljoin(self.base_url, self.test_page_urls[0]), 'depth': 1,
                                          'crawler': '0',
                                          'parser': '0', 'image_storage': '0'})
        self.assertEqual(response.status_code, 201)

    @override_settings(DEBUG=True, CELERY_TASK_ALWAYS_EAGER=True)
    def test_celery_task_parse_images(self):
        with HTTMock(request_mock):
            execute_task(_task_id=self.task2.id)
            for i in Page.objects.all().filter(task_id=self.task2.id):
                self.assertEqual(i.text, '')

    @override_settings(DEBUG=True, CELERY_TASK_ALWAYS_EAGER=True)
    def test_celery_task_parse_text(self):
        with HTTMock(request_mock):
            execute_task(_task_id=self.task3.id)
            for i in Page.objects.filter(task_id=self.task3.id):
                self.assertEqual(i.images.all().count(), 0)
                self.assertNotEqual(len(i.text), 0)
