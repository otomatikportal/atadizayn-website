import os

from django import template
from django.urls import reverse, translate_url
from django.utils.safestring import mark_safe
from django.utils.translation import override

from ..models import SiteAsset, SiteConfiguration

register = template.Library()


@register.simple_tag(takes_context=True)
def get_language_switch_url(context, language_code):
    request = context.get("request")
    if request is None:
        return "/"

    resolver_match = getattr(request, "resolver_match", None)
    url_name = getattr(resolver_match, "url_name", None)

    if url_name == "product-detail":
        product = context.get("product")
        category = context.get("category")
        if product is not None and category is None:
            category = getattr(product, "category", None)

        if product is not None and category is not None:
            category_slug = (getattr(category, f"slug_{language_code}", "") or "").strip() or category.slug
            product_slug = (getattr(product, f"slug_{language_code}", "") or "").strip() or product.slug
            with override(language_code):
                return reverse(
                    "product-detail",
                    kwargs={
                        "category_slug": category_slug,
                        "product_code": product_slug,
                    },
                )

    if url_name == "category-detail":
        category = context.get("category")
        if category is not None:
            category_slug = (getattr(category, f"slug_{language_code}", "") or "").strip() or category.slug
            with override(language_code):
                return reverse("category-detail", kwargs={"category_slug": category_slug})

    return translate_url(request.get_full_path(), language_code)


@register.simple_tag
def get_config(key, default=""):
    """
    Returns the value of a SiteConfiguration by key.
    Usage: {% get_config 'contact_email' 'info@example.com' %}
    """
    try:
        config = SiteConfiguration.objects.get(key=key)
        return config.value
    except SiteConfiguration.DoesNotExist:
        return default


@register.simple_tag
def asset_url(key):
    """
    Returns the URL of the site asset with the given key.
    Usage: {% asset_url 'my_key' %}
    """
    try:
        asset = SiteAsset.objects.get(key=key)
        if asset.file:
            return asset.file.url
        return ""
    except SiteAsset.DoesNotExist:
        return ""


@register.simple_tag
def render_asset(key, css_class=""):
    """
    Renders the asset based on its file type (Image or Video).
    Usage: {% render_asset 'hero_video' 'w-100' %}
    """
    try:
        asset = SiteAsset.objects.get(key=key)
        if not asset.file:
            return ""

        url = asset.file.url
        # Simple extension check
        ext = os.path.splitext(asset.file.name)[1].lower()

        if ext in [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"]:
            return mark_safe(f'<img src="{url}" alt="{asset.description or asset.key}" class="{css_class}">')
        elif ext in [".mp4", ".webm", ".ogg", ".mov"]:
            return mark_safe(f'<video src="{url}" class="{css_class}" autoplay loop muted playsinline></video>')
        else:
            # Fallback for generic files
            return mark_safe(
                f'<a href="{url}" class="{css_class}" target="_blank">{asset.description or asset.key}</a>'
            )

    except SiteAsset.DoesNotExist:
        return ""
