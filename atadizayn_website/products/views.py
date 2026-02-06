from django.shortcuts import get_object_or_404, render

from .models import Category, Product


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
	context = {
		"categories": categories,
		"carousel_categories": carousel_categories,
	}
	return render(request, "products/home.html", context)


def category_detail(request, category_slug: str):
	category = get_object_or_404(Category, slug=category_slug)
	products = category.products.all()
	other_categories = Category.objects.exclude(pk=category.pk).order_by("name")[:6]

	context = {
		"category": category,
		"products": products,
		"other_categories": other_categories,
	}
	return render(request, "products/category_detail.html", context)


def product_detail(request, category_slug: str, product_code: str):
	category = get_object_or_404(Category, slug=category_slug)
	product = get_object_or_404(Product, category=category, slug=product_code)

	context = {
		"category": category,
		"product": product,
	}
	return render(request, "products/product_detail.html", context)
