from django.urls import path

from . import views


urlpatterns = [
    path("part/", views.part_index, name="part_index"),
    path("stand/", views.stand_index, name="stand_index"),
    path("<slug:category_slug>/<slug:product_code>/", views.product_detail, name="product-detail"),
    path("<slug:category_slug>/", views.category_detail, name="category-detail"),
]
