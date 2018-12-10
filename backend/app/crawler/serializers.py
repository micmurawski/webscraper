from rest_framework import serializers

from app.media.serializers import ImageSerializer

from .models.page import Page
from .models.task import Task
from .tasks import execute_task


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'target_url', 'error', 'done')


class DetailedPageSerializer(PageSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Page
        fields = PageSerializer.Meta.fields + ('text', 'images')


class CreateTaskSerializer(serializers.ModelSerializer):
    pages_count = serializers.SerializerMethodField()
    succeed_at = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            'id', 'created_at', 'updated_at', 'target_url', 'depth', 'parser', 'crawler', 'images_storage', 'task_type',
            'done',
            'pages_count', 'succeed_at')
        read_only_fields = ('done', 'pages', 'created_at', 'updated_at')
        # write_only_fields = ('')

    def create(self, validated_data):
        obj = Task.objects.create(**validated_data)
        execute_task.apply_async(args=[obj.id, ], countdown=5)
        return obj

    def get_pages_count(self, obj):
        return obj.pages.count()

    def get_succeed_at(self, obj):
        if obj.pages.all().count() == 0:
            return None
        return sum([1 for i in obj.pages.all() if not i.error]) / obj.pages.all().count()


class RetrieveTaskSerializer(CreateTaskSerializer):
    parser = serializers.CharField(source='get_parser_display')
    crawler = serializers.CharField(source='get_crawler_display')
    task_type = serializers.CharField(source='get_task_type_display')


class DetailedTaskSerializer(RetrieveTaskSerializer):
    class Meta:
        model = Task
        fields = RetrieveTaskSerializer.Meta.fields
        read_only_fields = RetrieveTaskSerializer.Meta.read_only_fields
