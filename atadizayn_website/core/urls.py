from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("kitchen_sink/", TemplateView.as_view(template_name="kitchen_sink.html"), name="kitchen_sink"),
]
