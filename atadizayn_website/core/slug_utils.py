from django.conf import settings
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import get_language


SLUG_FIELDS = ("slug", "slug_en", "slug_tr")


def get_lang_code() -> str:
    return (get_language() or settings.LANGUAGE_CODE).split("-")[0]


def get_default_lang_code() -> str:
    default_lang = getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", settings.LANGUAGE_CODE)
    return (default_lang or settings.LANGUAGE_CODE).split("-")[0]


def build_slug_lookup_q(slug_value: str, slug_fields=SLUG_FIELDS) -> Q:
    value = (slug_value or "").strip()
    if not value:
        return Q(pk__in=[])

    query = Q()
    for field_name in slug_fields:
        query |= Q(**{field_name: value})
    return query


def build_active_language_slug_lookup_q(slug_value: str, slug_fields=SLUG_FIELDS) -> Q:
    value = (slug_value or "").strip()
    if not value:
        return Q(pk__in=[])

    lang_code = get_lang_code()
    language_field = f"slug_{lang_code}"

    if language_field not in slug_fields:
        language_field = "slug"

    return Q(**{language_field: value})


def build_unique_slug(
    instance,
    target_field: str,
    source_text: str,
    slug_fields=SLUG_FIELDS,
) -> str:
    base_slug = slugify(source_text or "", allow_unicode=False)
    if not base_slug:
        return ""

    queryset = type(instance).objects.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    candidate = base_slug
    suffix = 2
    while queryset.filter(build_slug_lookup_q(candidate, slug_fields=slug_fields)).exists():
        candidate = f"{base_slug}-{suffix}"
        suffix += 1

    return candidate


def get_translated_slug(instance, slug_fields=SLUG_FIELDS) -> str:
    lang_code = get_lang_code()
    default_lang = get_default_lang_code()

    preferred_fields = [f"slug_{lang_code}", f"slug_{default_lang}", "slug"]
    for field_name in preferred_fields:
        if field_name not in slug_fields:
            continue
        value = (getattr(instance, field_name, "") or "").strip()
        if value:
            return value

    for field_name in slug_fields:
        value = (getattr(instance, field_name, "") or "").strip()
        if value:
            return value

    return ""
