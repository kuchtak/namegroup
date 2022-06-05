from django.utils.translation import gettext as _
from django.db.models import Q

from rest_framework import serializers

from namegroup.folders.models import Folder


class FolderSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Folder
        fields = ('id', 'parent_id', 'name')

    def validate_parent_id(self, value):
        if value and not Folder.objects.filter(id=value).first():
            raise serializers.ValidationError(_("Parent folder doesn't exist."))
        return value

    def validate(self, attrs):
        parent_id = attrs.get("parent_id")
        name = attrs.get("name")

        query = Q(name=name)
        if parent_id is None:
            query &= Q(parent__isnull=True)
        else:
            query &= Q(parent_id=parent_id)

        if Folder.objects.filter(query).count():
            raise serializers.ValidationError(_("Folder is already created."))

        return attrs
