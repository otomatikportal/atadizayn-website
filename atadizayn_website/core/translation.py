from modeltranslation.translator import TranslationOptions, register

from .models import SiteConfiguration


@register(SiteConfiguration)
class SiteConfigurationTranslationOptions(TranslationOptions):
    required_languages = {
        "en": ("value",),
        "tr": ("value",),
    }
    fields = ("value",)
