from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.global_search, name="global_search"),
    path("kitchen_sink/", TemplateView.as_view(template_name="kitchen_sink.html"), name="kitchen_sink"),
]
