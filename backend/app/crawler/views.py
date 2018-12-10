from django.views.generic import TemplateView

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models.page import Page
from .models.task import Task
from .serializers import (
    CreateTaskSerializer,
    DetailedPageSerializer,
    DetailedTaskSerializer,
    PageSerializer,
    RetrieveTaskSerializer
)


class TaskViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    serializer_class = RetrieveTaskSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedTaskSerializer
        if self.action == 'create':
            return CreateTaskSerializer
        return super().get_serializer_class()


class PageViewSet(ReadOnlyModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedPageSerializer
        return super().get_serializer_class()

    def filter_queryset(self, queryset):
        task_pk = self.request.parser_context.get('kwargs').get('task_pk', None)
        if task_pk is not None:
            return super().filter_queryset(queryset).filter(task=task_pk)
        return super().filter_queryset(queryset)


class DocsView(TemplateView):
    template_name = 'docs.html'
