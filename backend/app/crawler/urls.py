from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from app.crawler import test_views

from .views import DocsView, PageViewSet, TaskViewSet

app_name = "crawler"

router = DefaultRouter()

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='tasks')
router.register(r'pages', PageViewSet, base_name='pages')
task_router = routers.NestedSimpleRouter(router, r'tasks', lookup='task')
task_router.register(r'pages', PageViewSet, base_name='pages')
nodes_router = routers.NestedSimpleRouter(task_router, r'pages', lookup='page')

urlpatterns = router.urls + task_router.urls + nodes_router.urls

urlpatterns += [path('docs/', DocsView.as_view(), name='docs'), ]
# Testing page

urlpatterns += [
    path('test/', test_views.home, name='home'),
    path('test/page_1/', test_views.page_1, name='page_1'),
    path('test/page_2/', test_views.page_2, name='page_2'),
    path('test/page_3/', test_views.page_3, name='page_3'),
    path('test/page_4/', test_views.page_4, name='page_4'),
]
