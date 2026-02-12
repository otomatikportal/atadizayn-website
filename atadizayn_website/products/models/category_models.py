from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from atadizayn_website.core.slug_utils import build_slug_lookup_q, build_unique_slug, get_default_lang_code, get_translated_slug

class Category(models.Model):
    COLLECTION_CHOICES = [
        ("stand", _("Standlar")),
        ("part", _("Parçalar")),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name=_("Ad"),
    )
    slug = AutoSlugField(
        populate_from="name",
        max_length=255,
        blank=True,
        unique=True,
        editable=True,
        verbose_name=_("Slug (url uç kısmı)"),
        help_text=_("Lütfen gerekmedikçe değiştirmeyin."),
    )
    collection = models.CharField(
        max_length=10,
        choices=COLLECTION_CHOICES,
        verbose_name=_("Koleksiyon"),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Açıklama"),
    )
    rich_text = CKEditor5Field(
        blank=True,
        verbose_name=_("Zengin metin"),
    )
    seo_canonical = models.URLField(
        blank=True,
        default="",
        editable=False,
        verbose_name=_("Kanonik URL"),
    )
    publish_date = models.DateField(
        default=timezone.localdate,
        verbose_name=_("Yayım tarihi"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma tarihi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme tarihi"))

    class Meta:
        ordering = ["name"]
        verbose_name = _("Kategori")
        verbose_name_plural = _("Kategoriler")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self._assign_missing_translated_slugs()

        if not (self.description or "").strip():
            plain_content = strip_tags((self.rich_text or "")).strip()
            if plain_content:
                self.description = plain_content

        super().save(*args, **kwargs)

        # Canonical URL logic (usually points to default language)
        canonical_url = self.get_absolute_url()
        type(self).objects.filter(pk=self.pk).update(seo_canonical=canonical_url)
        self.seo_canonical = canonical_url

    def get_absolute_url(self) -> str:
        category_slug = get_translated_slug(self)
        return reverse("category-detail", kwargs={"category_slug": category_slug})

    def clean(self):
        super().clean()
        english_name = (getattr(self, "name_en", None) or "").strip()
        if not english_name:
            raise ValidationError({"name_en": _("İngilizce ad zorunludur.")})

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

        reserved_slugs = {
            slug.lower()
            for slug in getattr(
                settings,
                "RESERVED_CATEGORY_SLUGS",
                (
                    "blog",
                    "admin",
                    "search",
                    "politikalar",
                    "i18n",
                    "ckeditor5",
                    "kitchen_sink",
                    "injection-products",
                    "pos-display-stands",
                ),
            )
        }
        slug_candidates = {
            "slug": (self.slug or slugify((self.name or "").strip(), allow_unicode=False)).strip().lower(),
            "slug_en": (
                (getattr(self, "slug_en", "") or slugify((english_name or "").strip(), allow_unicode=False))
                .strip()
                .lower()
            ),
            "slug_tr": (
                (getattr(self, "slug_tr", "") or slugify((turkish_name or "").strip(), allow_unicode=False))
                .strip()
                .lower()
            ),
        }

        errors = {}
        for field_name, slug_value in slug_candidates.items():
            if slug_value and slug_value in reserved_slugs:
                errors[field_name] = _("Bu slug kullanılamaz.")

        queryset = type(self).objects.all()
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        for field_name, slug_value in slug_candidates.items():
            if not slug_value:
                continue
            if queryset.filter(build_slug_lookup_q(slug_value)).exists():
                errors[field_name] = _("Bu slug başka bir kategoride kullanılıyor.")

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

class CategoryImage(models.Model):
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Kategori"),
    )
    image = models.ImageField(
        upload_to="categories/images/",
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
        verbose_name = _("Kategori görseli")
        verbose_name_plural = _("Kategori görselleri")

    def __str__(self) -> str:
        return f"{self.category.name} görseli"

    def save(self, *args, **kwargs):
        if not (self.alt_text or "").strip():
            self.alt_text = (self.category.name or "").strip()
        super().save(*args, **kwargs)


class CategoryDocument(models.Model):
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Kategori"),
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Başlık"),
    )
    file = models.FileField(
        upload_to="categories/documents/",
        verbose_name=_("Dosya"),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sıralama"),
    )

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = _("Kategori dokümanı")
        verbose_name_plural = _("Kategori dokümanları")

    def __str__(self) -> str:
        return self.title or f"{self.category.name} dokümanı"

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
