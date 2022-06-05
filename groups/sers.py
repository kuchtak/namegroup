from django.utils.translation import gettext as _
from django.db.models import Q

from rest_framework import serializers

from namegroup.folders.models import Folder
from namegroup.groups.models import Name
from namegroup.groups.utils import group_names
from namegroup.groups.utils import save_or_update_grouped_names


class NameAddSerializer(serializers.Serializer):
    folder_id = serializers.IntegerField(allow_null=True)

    def validate_folder_id(self, attr):
        if attr and not Folder.objects.filter(id=attr).count():
            raise serializers.ValidationError(_("Selected folder doesn't exist."))
        return attr


class NameCreateSerializer(NameAddSerializer):
    name = serializers.CharField()

    def create(self, validated_data):
        grouped_names = group_names([validated_data["name"]])
        save_or_update_grouped_names(grouped_names, folder_id=validated_data["folder_id"])
        return validated_data


class NameFileUploadSerializer(NameAddSerializer):
    file = serializers.FileField(write_only=True)

    def validate_folder_id(self, attr):
        if attr and not Folder.objects.filter(id=attr).count():
            raise serializers.ValidationError(_("Selected folder doesn't exist."))
        return attr

    def create(self, validated_data):
        grouped_names = group_names(self.context["request"].FILES["file"].
                                    read().decode().splitlines())
        save_or_update_grouped_names(grouped_names, folder_id=validated_data["folder_id"])
        return validated_data


class NameSerializer(serializers.ModelSerializer):
    prefix = serializers.CharField(source="group.prefix")

    class Meta:
        model = Name
        fields = ("prefix", "name", "folder_id")


class UpdateNameFolderSerializer(serializers.Serializer):
    to_folder_id = serializers.IntegerField(allow_null=True)
    from_folder_id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField()

    def validate(self, attrs):
        from_folder_id = attrs.get("from_folder_id")
        to_folder_id = attrs.get("to_folder_id")

        if from_folder_id == to_folder_id:
            raise serializers.ValidationError(
                _("You can't move name to the same folder.")
            )

        if to_folder_id and not Folder.objects.filter(id=to_folder_id).count():
            raise serializers.ValidationError(
                _("Folder you want to move to the name object doesn't exist.")
            )

        return attrs

    def update(self, instance, validated_data):
        # Check the name object with the same name exists in the
        # destination folder

        to_folder_id = validated_data.get("to_folder_id")

        dest_name_query = Q(name=instance.name)
        if not to_folder_id:
            dest_name_query &= Q(folder__isnull=True)
        else:
            dest_name_query &= Q(folder_id=to_folder_id)

        dest_obj = Name.objects.filter(dest_name_query).first()

        # We assume here that prefixes are calculated globally.
        # Not per folder.
        if dest_obj is not None:
            # If the same object exists in the destination folder
            # remove the name object form th folder with id from_folder_id.
            # We do not allow duplicates

            instance.delete()
            return dest_obj

        else:
            # Otherwise change the folder id in the instance to to_folder_id
            instance.folder_id = to_folder_id
            instance.save(update_fields=["folder_id"])
            return instance
