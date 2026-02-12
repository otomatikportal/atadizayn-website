from django.db import models
from django.utils.translation import gettext_lazy as _


class BrandCarouselImage(models.Model):
    """Model for brand logos in the homepage carousel"""

    image = models.FileField(upload_to="brands/carousel/", help_text="Brand logo image (PNG, JPG, SVG, etc.)")
    alt_text = models.CharField(max_length=255, help_text="Alternative text for accessibility")
    website_url = models.URLField(blank=True, null=True, help_text="Customer's website URL (optional)")
    is_active = models.BooleanField(default=True, help_text="Show/hide this brand in carousel")

    class Meta:
        verbose_name = "Brand Carousel Image"
        verbose_name_plural = "Brand Carousel Images"

    def __str__(self):
        return self.alt_text


class SiteAsset(models.Model):
    """Model for managing site-wide assets identifiable by a unique key"""

    key = models.SlugField(
        max_length=100,
        unique=True,
        help_text="Unique key to reference this asset in templates (e.g., 'hero_video', 'footer_logo')",
    )
    file = models.FileField(upload_to="assets/", help_text="Upload the asset file (Image, Video, PDF, etc.)")
    description = models.CharField(max_length=255, blank=True, help_text="Internal note about where this asset is used")

    class Meta:
        verbose_name = "Site Asset"
        verbose_name_plural = "Site Assets"

    def __str__(self):
        return self.key


class SiteConfiguration(models.Model):
    """Model for general key-value site configurations"""

    key = models.CharField(max_length=100, unique=True, help_text="Unique key for configuration (e.g., 'contact_email')")
    value = models.TextField(help_text="Configuration value")
    description = models.CharField(max_length=255, blank=True, help_text="Internal note about what this setting does")

    class Meta:
        verbose_name = _("Site konfigürasyonu")
        verbose_name_plural = _("Site konfigürasyonları")

    def __str__(self):
        return self.key
