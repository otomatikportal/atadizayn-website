from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView

from atadizayn_website.core.models import BrandCarouselImage, Policy
from atadizayn_website.products.models import Category, Product, ProductVariant


def global_search(request):
    query = request.GET.get("q")
    results = []

    if query:
        # We use icontains for "elastic" partial matching (e.g. "Bağ" matching "Bağlantı")
        # Search in Categories
        categories = (
            Category.objects.filter(
                Q(name__icontains=query)
                | Q(name_en__icontains=query)
                | Q(name_tr__icontains=query)
                | Q(description__icontains=query)
                | Q(description_en__icontains=query)
                | Q(description_tr__icontains=query)
                | Q(rich_text__icontains=query)
                | Q(rich_text_en__icontains=query)
                | Q(rich_text_tr__icontains=query)
            )
            .prefetch_related("images")
            .distinct()
        )

        # Search in Products
        products = (
            Product.objects.filter(
                Q(name__icontains=query)
                | Q(name_en__icontains=query)
                | Q(name_tr__icontains=query)
                | Q(description__icontains=query)
                | Q(description_en__icontains=query)
                | Q(description_tr__icontains=query)
                | Q(rich_text__icontains=query)
                | Q(rich_text_en__icontains=query)
                | Q(rich_text_tr__icontains=query)
            )
            .prefetch_related("images")
            .distinct()
        )

        # Search in Variants by Code or Size
        variants = (
            ProductVariant.objects.filter(Q(code__icontains=query) | Q(size__icontains=query))
            .select_related("product")
            .prefetch_related("product__images")
        )

        results = list(categories) + list(products) + list(variants)

    # Pagination
    paginator = Paginator(results, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/search_results.html", {"page_obj": page_obj, "query": query})


def home(request):
    categories = list(Category.objects.order_by("name").prefetch_related("images"))
    carousel_categories = []
    for category in categories:
        images = list(category.images.all())
        if not images:
            continue
        category.carousel_image = images[0]
        carousel_categories.append(category)
        if len(carousel_categories) >= 3:
            break

    # Get brand carousel images
    brands = BrandCarouselImage.objects.filter(is_active=True)

    context = {
        "categories": categories,
        "carousel_categories": carousel_categories,
        "brands": brands,
    }
    return render(request, "home.html", context)


class PolicyDetailView(DetailView):
    model = Policy
    template_name = "core/policy_detail.html"
    context_object_name = "policy"

    def get_queryset(self):
        return Policy.objects.filter(is_active=True)
