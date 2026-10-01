from django.urls import include, path

from . import views

app_name = "goals"

urlpatterns = [
    path("", views.goal_list, name="list"),
    path("goals/", include("goals.urls")),
]
