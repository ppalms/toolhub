import logging

from django.contrib import admin
import tagulous.admin
from tagulous import forms as tag_forms

from .models import ToolTaxonomy, ToolPhoto, UserTool


logger = logging.getLogger(__name__)


# temporary monkey patch until pr is merged
# https://github.com/radiac/django-tagulous/pull/58
render_super = tag_forms.TagWidgetBase.render

def replaced_render(self, name, value, attrs={}, renderer=None):
    return render_super(self, name, value, attrs=attrs)

tag_forms.TagWidgetBase.render = replaced_render


class UserToolAdmin(admin.ModelAdmin):
    list_display = ("title", "taxonomoies", "clearance")
    raw_id_fields = ("user",)


tagulous.admin.register(ToolTaxonomy)
tagulous.admin.register(UserTool, UserToolAdmin)


@admin.register(ToolPhoto)
class ToolPhotoAdmin(admin.ModelAdmin):
    raw_id_fields = ("tool", "uploading_user")


__all__ = []
