from django.db import models


class BrandCarouselImage(models.Model):
    """Model for brand logos in the homepage carousel"""
    icon_name = models.CharField(
        max_length=100,
        help_text="Bootstrap icon name (e.g., 'bi-microsoft')"
    )
    alt_text = models.CharField(
        max_length=255,
        help_text="Alternative text for accessibility (not translated)"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in carousel"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show/hide this brand in carousel"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Brand Carousel Image"
        verbose_name_plural = "Brand Carousel Images"

    def __str__(self):
        return self.alt_text
