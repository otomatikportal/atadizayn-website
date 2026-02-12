from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def part_index(request):
    # Annotate with the number of variants (SKUs) available
    categories = Category.objects.filter(collection="part").annotate(items_count=Count("products__variants"))
    context = {
        "categories": categories,
    }
    return render(request, "part_index.html", context)


def stand_index(request):
    # Annotate with the number of variants (SKUs) available
    categories = Category.objects.filter(collection="stand").annotate(items_count=Count("products__variants"))
    context = {
        "categories": categories,
    }
    return render(request, "stand_index.html", context)


def category_detail(request, category_slug: str):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.products.all()
    other_categories = Category.objects.exclude(pk=category.pk).order_by("name")[:6]

    context = {
        "category": category,
        "products": products,
        "other_categories": other_categories,
        "canonical_url": request.build_absolute_uri(category.get_absolute_url()),
    }
    return render(request, "products/category_detail.html", context)


def product_detail(request, category_slug: str, product_code: str):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_code)

    context = {
        "category": category,
        "product": product,
        "canonical_url": request.build_absolute_uri(product.get_absolute_url()),
    }
    return render(request, "products/product_detail.html", context)
