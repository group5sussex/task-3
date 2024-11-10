from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("submit", csrf_exempt(views.submit), name="submit"),
]