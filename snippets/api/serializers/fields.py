import os
import subprocess

from django.conf import settings
from django.template import defaultfilters as filters
from django.template.defaultfilters import urlencode

from rest_framework import serializers
from snippets.enums import StatusEnum

from snippets.template_backends.jinja2.globals import cropped_thumbnail, thumbnail


__all__ = (
    'CroppingThumbnailField', 'FileField', 'ImageField', 'PublishedRelationField', 'PretextField',
    'ThumbnailField', 'VideoField'
)


class CroppingThumbnailField(serializers.Field):
    def __init__(self, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        cropping_parameters = kwargs.pop('cropping_parameters', {})
        self.cropping_parameters = cropping_parameters
        super(CroppingThumbnailField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        result = cropped_thumbnail(value, self.field_name, **self.cropping_parameters)
        if result:
            return '%s%s' % (settings.MEDIA_URL, result)


class FileField(serializers.FileField):
    def to_representation(self, value):
        result = super(FileField, self).to_representation(value)
        if result:
            return '%s%s' % (settings.MEDIA_URL, urlencode(result))


class ImageField(serializers.ImageField):
    def to_representation(self, value):
        result = super(ImageField, self).to_representation(value)
        if result:
            return '%s%s' % (settings.MEDIA_URL, urlencode(result))


class PretextField(serializers.ReadOnlyField):
    def to_representation(self, value):
        result = super(PretextField, self).to_representation(value)
        if result:
            return filters.linebreaksbr(result)


class PublishedRelationField(serializers.Field):
    """"""
    def __init__(self, serializer_class, many=True, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        self.filters = kwargs.pop('filters', None)
        self.select_related = kwargs.pop('select_related', None)
        self.serializer_class = serializer_class
        self.many = many
        super(PublishedRelationField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        qs = None
        if self.many:
            qs = getattr(value, self.field_name).published()
            if self.filters:
                qs = qs.filter(self.filters)

            if self.select_related:
                qs = qs.select_related(*self.select_related)
        else:
            obj = getattr(value, self.field_name)
            if obj and obj.status == StatusEnum.PUBLIC:
                qs = obj

        if qs:
            return self.serializer_class(qs, many=self.many).data

        return [] if self.many else None


class ThumbnailField(serializers.Field):
    def __init__(self, thumbnail_parameters=None, image_field=None, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        self.thumbnail_parameters = thumbnail_parameters or {}
        self.image_field = image_field
        super(ThumbnailField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        field = self.image_field if self.image_field else self.field_name
        if hasattr(value, field) and getattr(value, field):
            result = thumbnail(getattr(value, field), **self.thumbnail_parameters)
            return result if result else None

        return None


class VideoField(serializers.FileField):
    def to_representation(self, value):
        source = super(VideoField, self).to_representation(value)
        if not source:
            return None

        source_path = os.path.join(settings.MEDIA_ROOT, source)
        if not os.path.exists(source_path):
            return None

        file = '.'.join(source.split('.')[:-1])
        file_path = os.path.join(settings.MEDIA_ROOT, file)
        file_url = os.path.join(settings.MEDIA_URL, file)
        result = []

        formats = {
            'mp4': '-q:v 1 -c:v libx264 -profile:v baseline -level 3.0',
            'm4v': '-q:v 1 -c:v libx264 -profile:v main -level 3.1',
            'webm': '-q:v 1 -c:v libvpx -quality good -cpu-used 0 -b:v 7000k -qmin 10 -qmax 42 '
                    '-maxrate 500k -bufsize 1500k -f webm',
            # 'ogv': '-codec:v libtheora'
        }

        for ext in formats:
            result_path = f'{file_path}.encoded.{ext}'
            result_url = f'{file_url}.encoded.{ext}'
            if not os.path.exists(result_path):
                args = f'-an {formats[ext]} -threads 4 -preset veryslow'
                cmd = f'ffmpeg -i {source_path} {args} {result_path}'
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                    shell=True
                )
                for line in process.stdout:
                    print(line)
            if ext == 'mp4':
                mime = None
            elif ext == 'm4v':
                mime = 'video/mp4'
            elif ext == 'ogv':
                mime = 'video/ogg'
            else:
                mime = f'video/{ext}'
            result.append({
                'type': mime,
                'url': result_url
            })

        return result
