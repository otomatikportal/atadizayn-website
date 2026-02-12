from modeltranslation.translator import TranslationOptions, register

from .models import BlogPost


@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    required_languages = {
        "tr": ("title",),
        "en": ("title",),
    }
    fields = (
        "title",
        "slug",
        "meta_description",
        "content",
    )
    fallback_languages = {"default": ("tr",), "en": ("tr",)}
    fallback_undefined = {
        "meta_description": "",
        "content": "<p>&nbsp;</p>",
    }
