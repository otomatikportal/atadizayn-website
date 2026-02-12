from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from atadizayn_website.core.slug_utils import build_slug_lookup_q, build_unique_slug, get_default_lang_code, get_translated_slug

class Product(models.Model):
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Kategori"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Ad"),
    )
    slug = AutoSlugField(
        populate_from="name",
        max_length=100,
        blank=True,
        unique=True,
        editable=True,
        verbose_name=_("Slug"),
        help_text=_("Lütfen gerekmedikçe değiştirmeyin."),
    )
    publish_date = models.DateField(
        default=timezone.localdate,
        verbose_name=_("Yayım tarihi"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Açıklama"),
    )
    rich_text = CKEditor5Field(
        blank=True,
        verbose_name=_("Zengin metin"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma tarihi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme tarihi"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Ürün")
        verbose_name_plural = _("Ürünler")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self._assign_missing_translated_slugs()

        if not (self.description or "").strip():
            plain_content = strip_tags((self.rich_text or "")).strip()
            if plain_content:
                self.description = plain_content

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        category_slug = get_translated_slug(self.category)
        product_slug = get_translated_slug(self)
        return reverse(
            "product-detail",
            kwargs={
                "category_slug": category_slug,
                "product_code": product_slug,
            },
        )

    def clean(self):
        super().clean()
        # Check English
        english_name = (getattr(self, "name_en", None) or "").strip()
        if not english_name:
            raise ValidationError({"name_en": _("İngilizce ad zorunludur.")})

        # Check Turkish
        turkish_name = (getattr(self, "name_tr", None) or "").strip()
        if not turkish_name:
            raise ValidationError({"name_tr": _("Türkçe ad zorunludur.")})

        description_value = (self.description or "").strip()
        content_value = strip_tags((self.rich_text or "")).strip()
        if not description_value and not content_value:
            raise ValidationError(
                {
                    "description": _("Açıklama veya içerik alanlarından en az biri doldurulmalıdır."),
                    "rich_text": _("Açıklama veya içerik alanlarından en az biri doldurulmalıdır."),
                }
            )

        slug_values = {
            "slug": (self.slug or "").strip(),
            "slug_en": (getattr(self, "slug_en", "") or "").strip(),
            "slug_tr": (getattr(self, "slug_tr", "") or "").strip(),
        }
        queryset = type(self).objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        errors = {}
        for field_name, slug_value in slug_values.items():
            if not slug_value:
                continue
            if queryset.filter(build_slug_lookup_q(slug_value)).exists():
                errors[field_name] = _("Bu slug başka bir üründe kullanılıyor.")

        if errors:
            raise ValidationError(errors)

    def _assign_missing_translated_slugs(self):
        for lang_code in ["en", "tr"]:
            name_value = (getattr(self, f"name_{lang_code}", "") or "").strip()
            if not name_value:
                continue
            slug_field = f"slug_{lang_code}"
            if not (getattr(self, slug_field, "") or "").strip():
                setattr(self, slug_field, build_unique_slug(self, slug_field, name_value))

        default_slug = (getattr(self, f"slug_{get_default_lang_code()}", "") or "").strip()
        if default_slug and not (self.slug or "").strip():
            self.slug = default_slug


class ProductImage(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Ürün"),
    )
    image = models.ImageField(
        upload_to="products/images/",
        verbose_name=_("Görsel"),
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Alternatif metin"),
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name=_("Birincil"),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıralama"),
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Ürün görseli")
        verbose_name_plural = _("Ürün görselleri")

    def __str__(self) -> str:
        return f"{self.product.name} görseli"

    def save(self, *args, **kwargs):
        if not (self.alt_text or "").strip():
            self.alt_text = (self.product.name or "").strip()
        super().save(*args, **kwargs)


class ProductDocument(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Ürün"),
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Başlık"),
    )
    file = models.FileField(
        upload_to="products/documents/",
        verbose_name=_("Dosya"),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıralama"),
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Ürün dokümanı")
        verbose_name_plural = _("Ürün dokümanları")

    def __str__(self) -> str:
        return self.title or f"{self.product.name} dokümanı"

    @property
    def icon_name(self):
        import os

        if not self.file:
            return "bi-file-earmark"
        name, ext = os.path.splitext(self.file.name)
        ext = ext.lower().replace(".", "")
        if ext == "pdf":
            return "bi-file-pdf"
        if ext in ["xls", "xlsx", "csv"]:
            return "bi-file-excel"
        if ext in ["doc", "docx"]:
            return "bi-file-word"
        if ext in ["jpg", "jpeg", "png", "gif", "webp"]:
            return "bi-file-earmark-image"
        if ext in ["zip", "rar", "7z"]:
            return "bi-file-zip"
        if ext == "txt":
            return "bi-file-text"
        return "bi-file-earmark"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name=_("Ürün"),
    )
    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Kod (SKU)"),
    )
    size = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Ölçü"),
    )
    package_weight = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Paket ağırlığı"),
    )
    package_size = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Paket ölçüsü"),
    )
    package_quantity = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Paket içi adet"),
    )
    minimum_order = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Minimum sipariş"),
    )

    class Meta:
        verbose_name = _("Ürün Varyantı")
        verbose_name_plural = _("Ürün Varyantları")
        ordering = ["code"]

    def __str__(self):
        return f"{self.product.name} - {self.code} ({self.size})"

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    @property
    def name(self):
        return f"{self.product.name} - {self.code}"

    @property
    def description(self):
        parts = []
        if self.size:
            parts.append(self.size)
        if self.package_quantity:
            parts.append(f"Paket: {self.package_quantity}")
        return " - ".join(parts)
