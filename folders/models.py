from django.db import models


class Folder(models.Model):
    parent = models.ForeignKey("folders.Folder", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)

    class Meta:
        unique_together = ('parent', 'name')
