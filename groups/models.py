from django.db import models

from namegroup.folders.models import Folder


class NameGroup(models.Model):
    prefix = models.CharField(max_length=128, unique=True)


class Name(models.Model):
    # We allow name to not belong to any folder
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True,
                               related_name="name_folder")
    group = models.ForeignKey(NameGroup, on_delete=models.CASCADE)
    name = models.TextField(null=True)

    class Meta:
        unique_together = ('folder', 'name')
