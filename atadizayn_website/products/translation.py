from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product, ProductVariant


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    required_languages = {
        "en": ("name",),
        "tr": ("name",),
    }
    fields = (
        "name",
        "slug",
        "description",
        "rich_text",
    )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    required_languages = {
        "en": ("name",),
        "tr": ("name",),
    }
    fields = (
        "name",
        "slug",
        "description",
        "rich_text",
    )


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    required_languages = ("en", "tr")
    fields = ("size",)  # Translate size (Small/Küçük)
