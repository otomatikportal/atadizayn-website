from mptt.templatetags.mptt_tags import cache_tree_children

from .models import Category


def footer_categories(request):
	categories = Category.objects.all()
	return {
		"footer_categories": cache_tree_children(categories),
	}
