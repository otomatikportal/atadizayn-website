from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:category_slug>/<slug:product_code>/", views.product_detail, name="product-detail"),
    path("<slug:category_slug>/", views.category_detail, name="category-detail"),
]
