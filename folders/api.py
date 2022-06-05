from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView

from namegroup.folders.models import Folder
from namegroup.folders.sers import FolderSerializer


class FolderCreateApiView(CreateAPIView):
    serializer_class = FolderSerializer


# TODO: add folder filterig (per parent_id)
class FolderListApiViews(ListAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        parent_id = self.request.data.get('parent_id')
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)

        return queryset
