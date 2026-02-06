from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    required_languages = ("en",)
    fields = (
        "name",
        "description",
        "rich_text",
        "color",
    )


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    required_languages = ("en",)
    fields = (
        "name",
        "description",
        "rich_text",
    )
