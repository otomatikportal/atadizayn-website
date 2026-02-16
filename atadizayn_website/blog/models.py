from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from atadizayn_website.core.slug_utils import (
    build_slug_lookup_q,
    get_default_lang_code,
    get_translated_slug,
)


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Taslak')),
        ('published', _('Yayında')),
    )
    COLLECTION_CHOICES = (
        ('policy', _('Politikalar')),
        ('announcement', _('Duyurular')),
        ('post', _('Blog paylaşımları')),
        ('corporate', _('Kurumsal')),
    )

    # --- Core Page Data ---
    title = models.CharField(
        max_length=255,
        verbose_name=_("Sayfa Başlığı"),
        help_text=_("Sayfanın H1 başlığı ve tarayıcı sekmesinde görünen isim.")
    )
    slug = AutoSlugField(
        populate_from="title",
        max_length=255,
        unique=True,
        blank=True,
        editable=True,
        verbose_name=_("Slug"),
        help_text=_("Lütfen gerekmedikçe değiştirmeyin."),
    )
    # Merged logic: This serves as both the SEO description and the short summary
    meta_description = models.TextField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name=_("Meta / Kısa Açıklama"),
        help_text=_("Girilmediyse içerikten çekilir, daha güçlü SEO için giriniz ancak zorunlu değildir."),
    )
    content = CKEditor5Field(
        verbose_name=_("Sayfa İçeriği"),
        blank=True,
        null=True,
        config_name='page_design',
    )

    # --- Visuals ---
    cover_image = models.ImageField(
        upload_to="blog/covers/",
        blank=True,
        null=True,
        verbose_name=_("Kapak Görseli"),
    )
    cover_image_alt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Kapak Görseli Alt Metni"),
    )
    collection = models.CharField(
        max_length=20,
        choices=COLLECTION_CHOICES,
        default='post',
        null=True,
        blank=True,
        verbose_name=_("Koleksiyon"),
    )

    # --- Publication ---
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        null=True,
        blank=True,
        verbose_name=_("Durum")
    )
    publish_date = models.DateTimeField(
        default=timezone.now,
        null=True,
        blank=True,
        verbose_name=_("Yayım Tarihi"),
        db_index=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Tarihi"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme Tarihi"))

    class Meta:
        ordering = ['-publish_date']
        verbose_name = _('Blog Yazısı')
        verbose_name_plural = _('Blog Yazıları')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-fill alt text if missing
        if self.cover_image and not self.cover_image_alt:
            self.cover_image_alt = self.title

        if not (self.meta_description or "").strip():
            plain_content = strip_tags(self.content or "").strip()
            if plain_content:
                self.meta_description = plain_content[:160]

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        current_slug = get_translated_slug(self)
        return reverse("blog-detail", kwargs={"slug": current_slug})

    def clean(self):
        super().clean()
        default_lang = get_default_lang_code()
        description_field = f"meta_description_{default_lang}"
        content_field = f"content_{default_lang}"

        description_value = (getattr(self, description_field, None) or self.meta_description or "").strip()
        content_value = getattr(self, content_field, None) or self.content or ""

        errors = {}
        if not description_value:
            errors[description_field] = _("Varsayılan dilde açıklama zorunludur.")
        if not self._has_visible_text(content_value):
            errors[content_field] = _("Varsayılan dilde içerik zorunludur.")

        if errors:
            raise ValidationError(errors)

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
            "slug": (self.slug or slugify((self.title or "").strip(), allow_unicode=False)).strip().lower(),
            "slug_en": (
                (
                    getattr(self, "slug_en", "")
                    or slugify(((getattr(self, "title_en", None) or "").strip()), allow_unicode=False)
                )
                .strip()
                .lower()
            ),
            "slug_tr": (
                (
                    getattr(self, "slug_tr", "")
                    or slugify(((getattr(self, "title_tr", None) or "").strip()), allow_unicode=False)
                )
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
                errors[field_name] = _("Bu slug başka bir blog yazısında kullanılıyor.")

        if errors:
            raise ValidationError(errors)

        if self.cover_image:
            width = getattr(self.cover_image, "width", None)
            height = getattr(self.cover_image, "height", None)
            if width and height and (width != height * 3):
                raise ValidationError({"cover_image": _("Kapak görseli 3:1 oranında olmalıdır.")})

    @staticmethod
    def _has_visible_text(value: str) -> bool:
        plain_value = strip_tags(value or "").replace("\xa0", " ").strip()
        return bool(plain_value)
