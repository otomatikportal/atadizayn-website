from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.home, name="home"),
    path("<path:category_path>/<slug:product_code>/", views.product_detail, name="product-detail"),
    path("<path:category_path>/", views.category_detail, name="category-detail"),
]
