from django import template
from django.utils.safestring import mark_safe
from ..models import SiteAsset
import os

register = template.Library()

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
        
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']:
            return mark_safe(f'<img src="{url}" alt="{asset.description or asset.key}" class="{css_class}">')
        elif ext in ['.mp4', '.webm', '.ogg', '.mov']:
             return mark_safe(f'<video src="{url}" class="{css_class}" autoplay loop muted playsinline></video>')
        else:
            # Fallback for generic files
            return mark_safe(f'<a href="{url}" class="{css_class}" target="_blank">{asset.description or asset.key}</a>')
            
    except SiteAsset.DoesNotExist:
        return ""
