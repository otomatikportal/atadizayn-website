from django.urls import path

from .views import BlogDetailView

urlpatterns = [
    path("<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
