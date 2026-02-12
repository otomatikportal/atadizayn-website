from django.urls import path

from .views import BlogDetailView, blog_collection_index, blog_index

urlpatterns = [
    path("", blog_index, name="blog-index"),
    path("duyurular/", blog_collection_index, {"collection": "announcement"}, name="blog-announcements"),
    path("politikalar/", blog_collection_index, {"collection": "policy"}, name="blog-policies"),
    path("kurumsal/", blog_collection_index, {"collection": "corporate"}, name="blog-corporate"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
