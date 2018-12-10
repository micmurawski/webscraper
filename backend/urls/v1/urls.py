from django.urls import include, path

urlpatterns = [
    path('', include('app.crawler.urls', namespace='crawler'), name="crawler"),
]
