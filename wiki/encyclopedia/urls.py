from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search",views.Search, name="search"),
    path("create",views.create, name="create"),
    path("wiki/",views.random_page, name="random"),
    path("edit/<str:title>",views.edit,name="edit")
]
