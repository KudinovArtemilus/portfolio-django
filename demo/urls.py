from django.urls import path

from . import views

app_name = "demo"

urlpatterns = [
    path("", views.page, name="page"),
    path("live/", views.live, name="live"),
]
