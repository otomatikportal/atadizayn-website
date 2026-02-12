from django.urls import path

from .views import BlogDetailView, blog_index

urlpatterns = [
    path("", blog_index, name="blog-index"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
