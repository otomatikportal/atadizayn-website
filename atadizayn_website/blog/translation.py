from modeltranslation.translator import TranslationOptions, register

from .models import BlogPost


@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    required_languages = {
        "en": ("title",),
        "tr": ("title",),
    }
    fields = (
        "title",
        "slug",
        "meta_description",
        "content",
        "cover_image_alt",
    )
