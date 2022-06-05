from django.urls import path

from namegroup.groups.api import NameCreateApiView
from namegroup.groups.api import NameFileUploadApiView
from namegroup.groups.api import MoveNameToFolderUpdateApiView
from namegroup.groups.api import GroupedNameListApiView


urlpatterns = [
    path("add", NameCreateApiView.as_view()),
    path("upload", NameFileUploadApiView.as_view()),
    path("update", MoveNameToFolderUpdateApiView.as_view()),
    path("list",  GroupedNameListApiView.as_view()),
]
