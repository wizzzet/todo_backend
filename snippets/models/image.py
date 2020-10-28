from django.conf import settings
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.exceptions import EasyThumbnailsError
from easy_thumbnails.files import get_thumbnailer


class ImageMixin(models.Model):
    image_field = 'image'
    image_size = (70, 40)

    def image_thumb(self):
        image = getattr(self, self.image_field)
        if image and not isinstance(image, ImageFieldFile):
            return format_html('<img src="%s" alt="" style="max-width:%spx;max-height:%spx;">' % (
                image.url, self.image_size[0], self.image_size[1]
            ))
        else:
            try:
                return format_html(
                    '<img src="%s" alt="" />' % get_thumbnailer(
                        getattr(self, self.image_field)
                    ).get_thumbnail({
                        'size': self.image_size,
                        'detail': True,
                    }).url if image else '<img src="%simages/blank.gif" alt="" '
                    'style="max-width:%spx;max-height:%spx;" />' % (
                        settings.STATIC_URL, self.image_size[0], self.image_size[1]
                    )
                )
            except (OSError, EasyThumbnailsError):
                return ''

    image_thumb.short_description = _('Изображение')

    class Meta:
        abstract = True
