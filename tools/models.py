"""
Tools are singular physical objects or process grouped physical
objects that are used to perform a specific task

they have multiple taxonomies
Process, what sorta processes this tool can be used for
Automation, what level of automation this tool contains for accomplishing the process?
Approach,
Viewpoint
"""
from catalog import Catalog
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from tagulous.models import TagField, TagTreeModel

from tools.querysets import UserToolQuerySet


class ToolTaxonomy(TagTreeModel):
    """A generic way of describing a tool, the top level is the base taxonomy"""

    # order = models.IntegerField(blank=False, default=0)

    # Published state
    # Allows users to submit new taxonomies that are evaluated and approved
    class State(Catalog):
        _attrs = "value", "label"
        in_review = 0, _("in review")
        approved = 1, _("approved")
        rejected = 2, _("rejected")

    state = models.PositiveSmallIntegerField(
        _("State"), choices=State._zip("value", "label"), default=State.in_review.value
    )

    class Meta:
        verbose_name = _("Tool Taxonomy")
        verbose_name_plural = _("Tool Taxonomies")

    # class TagMeta:
    #     force_lowercase = True


class UserTool(TitleDescriptionModel, TimeStampedModel):
    """A tool owned by a User"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='tools')
    taxonomoies = TagField(to=ToolTaxonomy, blank=True, related_name="tools")

    class Visibility(Catalog):
        _attrs = "value", "label"
        private = 0, _("Visible to owner")
        cleared = 1, _('Visible to cleared')
        public = 2, _("Visbile to everyone")

    visibility = models.PositiveSmallIntegerField(
        _('Visibility'),
        choices=Visibility._zip('value', 'label'),
        default=Visibility.public.value,
    )

    class Clearance(Catalog):
        _attrs = "value", "label"
        none = 0, _("No clearance")
        owner = 1, _("Owner approved")
        cleared = 2, _("Cleared-user approved")

    clearance = models.PositiveSmallIntegerField(
        _("Clearance"),
        choices=Clearance._zip("value", "label"),
        default=Clearance.none.value,
    )

    objects = UserToolQuerySet.as_manager()

    def __str__(self):
        return self.title


class ToolHistory(TimeStampedModel):
    class Actions(Catalog):
        _attrs = "value", "label"
        create = 0, 'Create'
        borrow = 1, 'Borrow'
        return_ = 2, 'Return'
        decommission = 3, 'Decommission'
        reinstate = 4, 'Reinstate'

    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='tool_history')
    action = models.PositiveSmallIntegerField(choices=Actions._zip('value', 'label'))


class ClearancePermission(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name='permissions')
    cleared_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="given_tool_permissions",
    )
    cleared_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tool_permissions",
    )


class ToolPhoto(TimeStampedModel):
    tool = models.ForeignKey(UserTool, on_delete=models.CASCADE, related_name='photos')
    uploading_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='uploaded_photos'
    )
    file = models.FileField()
    title = models.CharField(max_length=255, blank=True)