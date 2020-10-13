from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="home"),
    path("wiki/<str:entry>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("create_entry", views.createNew, name="new_entry"),
    path("edit_entry/<str:entry>", views.editEntry, name="editor"),
]
