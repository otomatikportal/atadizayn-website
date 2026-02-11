from modeltranslation.translator import TranslationOptions, register
from .models import Category, Product, ProductVariant


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    # This enforces validation in the Admin panel and Forms
    required_languages = ("en", "tr")
    fields = (
        "name",
        "description",
        "rich_text",
    )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    # This enforces validation in the Admin panel and Forms
    required_languages = ("en", "tr")
    fields = (
        "name",
        "description",
        "rich_text",
    )


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    required_languages = ("en", "tr")
    fields = ("size",)  # Translate size (Small/Küçük)
