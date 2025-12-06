from django.urls import path
from .views import MessageCreateAPI

urlpatterns = [
    path("message/", MessageCreateAPI.as_view()),
]
