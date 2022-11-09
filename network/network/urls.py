
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<int:user_id>/newpost",views.newPost, name="newPost"),
    path("following/<int:user_id>", views.following, name="following"),
    path("posts/<int:post_id>/edit", views.edit, name='edit'),
    url(r'^likepost/$', views.like, name='like-post')
    
]
