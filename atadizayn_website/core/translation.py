from modeltranslation.translator import register, TranslationOptions
from .models import Policy, SiteConfiguration


@register(SiteConfiguration)
class SiteConfigurationTranslationOptions(TranslationOptions):
    required_languages = ("en", "tr")
    fields = ("value",)


@register(Policy)
class PolicyTranslationOptions(TranslationOptions):
    # Rule: name is required in both, content (Rich Text) is optional
    required_languages = {
        "en": ("name",),
        "tr": ("name",),
    }
    fields = ("name", "content")
