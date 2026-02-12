from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


def _build_unique_slug(instance, field_name: str, source_text: str) -> str:
    base_slug = slugify(source_text or "", allow_unicode=False)
    if not base_slug:
        return ""

    candidate = base_slug
    suffix = 2
    queryset = type(instance).objects.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(**{field_name: candidate}).exists():
        candidate = f"{base_slug}-{suffix}"
        suffix += 1
    return candidate


def _get_lang_code() -> str:
    return (get_language() or settings.LANGUAGE_CODE).split("-")[0]


def _get_default_lang_code() -> str:
    default_lang = getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", settings.LANGUAGE_CODE)
    return (default_lang or settings.LANGUAGE_CODE).split("-")[0]

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
    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,  # Recommended to add unique=True if using name-based slugs
        editable=False,
        verbose_name=_("Slug"),
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
        if self._state.adding:
            self._assign_translated_slugs_on_create()
        else:
            self._lock_slugs_on_update()

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        lang_code = _get_lang_code()
        default_lang = _get_default_lang_code()
        category_slug = (
            (getattr(self.category, f"slug_{lang_code}", "") or "").strip()
            or (getattr(self.category, f"slug_{default_lang}", "") or "").strip()
            or self.category.slug
        )
        product_slug = (
            (getattr(self, f"slug_{lang_code}", "") or "").strip()
            or (getattr(self, f"slug_{default_lang}", "") or "").strip()
            or self.slug
        )
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

    def _assign_translated_slugs_on_create(self):
        for lang_code in ["en", "tr"]:
            name_value = (getattr(self, f"name_{lang_code}", "") or "").strip()
            if not name_value:
                continue
            slug_field = f"slug_{lang_code}"
            if not (getattr(self, slug_field, "") or "").strip():
                setattr(self, slug_field, _build_unique_slug(self, slug_field, name_value))

        default_slug = (getattr(self, f"slug_{_get_default_lang_code()}", "") or "").strip()
        if default_slug:
            self.slug = default_slug

    def _lock_slugs_on_update(self):
        original = type(self).objects.get(pk=self.pk)
        for field_name in ("slug", "slug_en", "slug_tr"):
            setattr(self, field_name, getattr(original, field_name, ""))


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
