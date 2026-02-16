from django.db import models
from django.utils.translation import gettext_lazy as _


class BrandCarouselImage(models.Model):
    """Model for brand logos in the homepage carousel"""

    image = models.FileField(
        upload_to="brands/carousel/",
        help_text=_("Marka logo görseli (PNG, JPG, SVG vb.)"),
    )
    alt_text = models.CharField(
        max_length=255,
        help_text=_("Erişilebilirlik için alternatif metin"),
    )
    website_url = models.URLField(
        blank=True,
        default="",
        help_text=_("Müşteri web sitesi URL'si (isteğe bağlı)"),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("Bu markayı kaydırıcıda göster/gizle"),
    )

    class Meta:
        verbose_name = _("Marka Şerit Görseli")
        verbose_name_plural = _("Marka Şerit Görselleri")

    def __str__(self):
        return self.alt_text


class SiteAsset(models.Model):
    """Model for managing site-wide assets identifiable by a unique key"""

    key = models.SlugField(
        max_length=100,
        unique=True,
        help_text=_("Şablonlarda bu varlığa referans vermek için benzersiz anahtar (örn. 'hero_video', 'footer_logo')"),
    )
    file = models.FileField(
        upload_to="assets/",
        help_text=_("Varlık dosyasını yükleyin (Resim, Video, PDF vb.)"),
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Bu varlığın nerede kullanıldığına dair dahili not"),
    )

    class Meta:
        verbose_name = _("Site Varlığı")
        verbose_name_plural = _("Site Varlıkları")

    def __str__(self):
        return self.key


class SiteConfiguration(models.Model):
    """Model for general key-value site configurations"""

    key = models.CharField(
        max_length=100,
        unique=True,
        help_text=_("Konfigürasyon için benzersiz anahtar (örn. 'contact_email')"),
    )
    value = models.TextField(help_text=_("Konfigürasyon değeri"))
    description = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Bu ayarın ne yaptığını anlatan dahili not"),
    )

    class Meta:
        verbose_name = _("Site konfigürasyonu")
        verbose_name_plural = _("Site konfigürasyonları")

    def __str__(self):
        return self.key
