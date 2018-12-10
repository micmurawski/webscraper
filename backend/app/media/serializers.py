from django.conf import settings

from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from .models import Image


class ImageSerializer(ModelSerializer):
    url = SerializerMethodField()
    storage = CharField(source='get_storage_display')

    class Meta:
        model = Image
        fields = ('id', 'url', 'storage',)

    def get_url(self, obj):
        if obj.get_storage_display() in ('local', 'LOCAL'):
            return self.context.get("request").build_absolute_uri(obj.url)
        else:
            return f"https://{settings.UPLOAD_APP[obj.get_storage_display()]['BASE_URL']}{obj.url}"
