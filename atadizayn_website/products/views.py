from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q
from .models import Category, Product, ProductVariant


def global_search(request):
    query = request.GET.get("q")
    results = []
    
    if query:
        # Search in Categories
        categories = Category.objects.annotate(
            search=SearchVector(
                "name", "name_en", "name_tr",
                "description", "description_en", "description_tr",
                "rich_text", "rich_text_en", "rich_text_tr"
            ),
        ).filter(search=query).distinct()
        
        # Search in Products
        products = Product.objects.annotate(
            search=SearchVector(
                "name", "name_en", "name_tr",
                "description", "description_en", "description_tr",
                "rich_text", "rich_text_en", "rich_text_tr",
                # Removed variants__code to rely on direct variant search
            ),
        ).filter(search=query).distinct()

        # Search in Variants
        # Use simple icontains for Code to ensure partial matching (e.g. "1.100" matching "1.100.0015")
        # And SearchVector for other text fields if needed
        variants = ProductVariant.objects.annotate(
            search=SearchVector("size"),
        ).filter(
            Q(code__icontains=query) | Q(search=query)
        ).select_related("product")
        
        results = list(categories) + list(products) + list(variants)
    
    # Pagination
    paginator = Paginator(results, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "products/search_results.html", {"page_obj": page_obj, "query": query})


def part_index(request):
    # Annotate with the number of variants (SKUs) available
    categories = Category.objects.filter(collection="part").annotate(
        items_count=Count("products__variants")
    )
    context = {
        "categories": categories,
        "collection_type": "part",
    }
    return render(request, "part_index.html", context)


def stand_index(request):
    # Annotate with the number of variants (SKUs) available
    categories = Category.objects.filter(collection="stand").annotate(
        items_count=Count("products__variants")
    )
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
