from modeltranslation.translator import TranslationOptions, register

from .models import Policy, SiteConfiguration


@register(SiteConfiguration)
class SiteConfigurationTranslationOptions(TranslationOptions):
    required_languages = {
        "en": ("value",),
        "tr": ("value",),
    }
    fields = ("value",)


@register(Policy)
class PolicyTranslationOptions(TranslationOptions):
    # Rule: name is required in both, content (Rich Text) is optional
    required_languages = {
        "en": ("name",),
        "tr": ("name", "content"),
    }
    fields = ("name", "content")
    fallback_languages = {"default": ("tr",), "en": ("tr",)}
    fallback_undefined = {"content": "<p>&nbsp;</p>"}
