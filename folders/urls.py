from django.urls import path

from namegroup.folders.api import FolderCreateApiView
from namegroup.folders.api import FolderListApiViews


urlpatterns = [
    path("add", FolderCreateApiView.as_view()),
    path("list",  FolderListApiViews.as_view()),
]
