from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q
from .models import Category, Product, ProductVariant


def part_index(request):
    # Annotate with the number of variants (SKUs) available
    categories = Category.objects.filter(collection="part").annotate(items_count=Count("products__variants"))
    context = {
        "categories": categories,
        "collection_type": "part",
    }
    return render(request, "part_index.html", context)


def stand_index(request):
    # Annotate with the number of variants (SKUs) available
    categories = Category.objects.filter(collection="stand").annotate(items_count=Count("products__variants"))
    context = {
        "categories": categories,
        "collection_type": "stand",
    }
    # Reusing the same template as it is generic enough now
    return render(request, "part_index.html", context)


def category_detail(request, category_slug: str):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.products.all()
    other_categories = Category.objects.exclude(pk=category.pk).order_by("name")[:6]

    context = {
        "category": category,
        "products": products,
        "other_categories": other_categories,
        "canonical_url": category.seo_canonical,
    }
    return render(request, "products/category_detail.html", context)


def product_detail(request, category_slug: str, product_code: str):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_code)

    context = {
        "category": category,
        "product": product,
        "canonical_url": product.get_absolute_url(),
    }
    return render(request, "products/product_detail.html", context)
