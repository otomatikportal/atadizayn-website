from modeltranslation.translator import TranslationOptions, register

from .models import Category, Product, ProductVariant


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    required_languages = {
        "tr": ("name",),
        "en": ("name",),
    }
    fields = (
        "name",
        "slug",
        "description",
        "rich_text",
    )
    fallback_languages = {"default": ("tr",), "en": ("tr",)}
    fallback_undefined = {
        "description": "",
        "rich_text": "<p>&nbsp;</p>",
    }


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    required_languages = {
        "tr": ("name",),
        "en": ("name",),
    }
    fields = (
        "name",
        "slug",
        "description",
        "rich_text",
    )
    fallback_languages = {"default": ("tr",), "en": ("tr",)}
    fallback_undefined = {
        "description": "",
        "rich_text": "<p>&nbsp;</p>",
    }


@register(ProductVariant)
class ProductVariantTranslationOptions(TranslationOptions):
    required_languages = {
        "tr": ("size",),
        "en": ("size",),
    }
    fields = ("size",)  # Translate size (Small/Küçük)
