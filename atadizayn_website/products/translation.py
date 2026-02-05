from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
        "rich_text",
        "seo_title",
        "seo_description",
    )


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "description",
        "rich_text",
        "seo_title",
        "seo_description",
    )
