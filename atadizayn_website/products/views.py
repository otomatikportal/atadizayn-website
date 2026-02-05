from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
	root_categories = Category.objects.root_nodes()
	context = {
		"root_categories": root_categories,
	}
	return render(request, "products/home.html", context)


def _resolve_category_path(category_path: str) -> Category:
	segments = [segment for segment in category_path.split("/") if segment]
	if not segments:
		raise Http404("Category path is empty.")

	parent = None
	category = None
	for slug in segments:
		category = get_object_or_404(Category, parent=parent, slug=slug)
		parent = category

	return category


def category_detail(request, category_path: str):
	category = _resolve_category_path(category_path)
	children = category.get_children()
	products = category.products.all()
	template_name = "products/category_leaf.html" if category.is_leaf_node() else "products/category_detail.html"

	context = {
		"category": category,
		"children": children,
		"products": products,
	}
	return render(request, template_name, context)


def product_detail(request, category_path: str, product_code: str):
	category = _resolve_category_path(category_path)
	try:
		product = Product.objects.get(category=category, code=product_code)
	except Product.DoesNotExist:
		fallback_path = f"{category_path}/{product_code}"
		fallback_category = _resolve_category_path(fallback_path)
		children = fallback_category.get_children()
		products = fallback_category.products.all()
		template_name = (
			"products/category_leaf.html" if fallback_category.is_leaf_node() else "products/category_detail.html"
		)
		context = {
			"category": fallback_category,
			"children": children,
			"products": products,
		}
		return render(request, template_name, context)

	context = {
		"category": category,
		"product": product,
	}
	return render(request, "products/product_detail.html", context)
