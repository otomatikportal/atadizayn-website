from .models import Category


def footer_categories(request):
    categories_by_collection = {}
    for choice_value, choice_label in Category.COLLECTION_CHOICES:
        categories_by_collection[choice_value] = {
            "label": choice_label,
            "categories": Category.objects.filter(collection=choice_value).order_by("name"),
        }
    return {"footer_categories_by_collection": categories_by_collection}
