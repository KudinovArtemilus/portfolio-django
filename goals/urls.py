from django.urls import path

from . import views

app_name = "goals"

urlpatterns = [
    path("", views.goal_list, name="list"),
    path("<slug:slug>/", views.goal_detail, name="detail"),
]
