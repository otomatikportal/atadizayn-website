from django.urls import path

from . import views

urlpatterns = [
    path("injection-products/", views.part_index, name="part_index"),
    path("pos-display-stands/", views.stand_index, name="stand_index"),
    path("<slug:category_slug>/<slug:product_code>/", views.product_detail, name="product-detail"),
    path("<slug:category_slug>/", views.category_detail, name="category-detail"),
]
