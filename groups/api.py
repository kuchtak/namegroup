from django.db.models import Q
from django.utils.translation import gettext as _

from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound

from namegroup.groups.sers import NameCreateSerializer
from namegroup.groups.sers import NameFileUploadSerializer
from namegroup.groups.sers import UpdateNameFolderSerializer
from namegroup.groups.sers import NameSerializer

from namegroup.groups.models import Name
from namegroup.folders.models import Folder


class NameCreateApiView(CreateAPIView):
    serializer_class = NameCreateSerializer


class NameFileUploadApiView(CreateAPIView):
    serializer_class = NameFileUploadSerializer


class MoveNameToFolderUpdateApiView(UpdateAPIView):
    serializer_class = UpdateNameFolderSerializer

    def get_object(self):
        from_folder_id = self.request.data.get("from_folder_id")
        name = self.request.data.get("name")

        if from_folder_id and not Folder.objects.filter(id=from_folder_id).count():
            raise NotFound(
                _("Folder you want to move from the name object doesn't exist.")
            )

        if not name:
            raise NotFound(_("Please provide the object name."))

        name_query = Q(name=name)
        if not from_folder_id:
            name_query &= Q(folder__isnull=True)
        else:
            name_query &= Q(folder_id=from_folder_id)

        name_obj = Name.objects.filter(name_query).first()
        if name_obj is None:
            raise NotFound(
                _("Name object you want to move doesn't exist")
            )

        return name_obj


class GroupedNameListApiView(ListAPIView):
    serializer_class = NameSerializer
    queryset = Name.objects.all()
