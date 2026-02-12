from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from atadizayn_website.core.slug_utils import (
    build_slug_lookup_q,
    build_unique_slug,
    get_default_lang_code,
    get_translated_slug,
)


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Taslak')),
        ('published', _('Yayında')),
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
        verbose_name=_("Meta / Kısa Açıklama"),
        help_text=_("Girilmediyse içerikten çekilir, daha güçlü SEO için giriniz ancak zorunlu değildir."),
    )
    content = CKEditor5Field(
        verbose_name=_("Sayfa İçeriği"),
        blank=True,
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
        verbose_name=_("Kapak Görseli Alt Metni"),
    )

    # --- Publication ---
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_("Durum")
    )
    publish_date = models.DateTimeField(
        default=timezone.now,
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

        self._assign_missing_slugs()

        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        current_slug = get_translated_slug(self)
        return reverse("blog-detail", kwargs={"slug": current_slug})

    def clean(self):
        super().clean()
        english_title = (getattr(self, "title_en", None) or "").strip()
        if not english_title:
            raise ValidationError({"title_en": _("İngilizce başlık zorunludur.")})

        turkish_title = (getattr(self, "title_tr", None) or "").strip()
        if not turkish_title:
            raise ValidationError({"title_tr": _("Türkçe başlık zorunludur.")})

        description_value = (self.meta_description or "").strip()
        content_value = strip_tags(self.content or "").strip()
        if not description_value and not content_value:
            raise ValidationError(
                {
                    "meta_description": _("Açıklama veya içerik alanlarından en az biri doldurulmalıdır."),
                    "content": _("Açıklama veya içerik alanlarından en az biri doldurulmalıdır."),
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
                errors[field_name] = _("Bu slug başka bir blog yazısında kullanılıyor.")

        if errors:
            raise ValidationError(errors)

    def _assign_missing_slugs(self):
        for lang_code in ["en", "tr"]:
            title_value = (getattr(self, f"title_{lang_code}", "") or "").strip()
            if not title_value:
                continue

            slug_field = f"slug_{lang_code}"
            if not (getattr(self, slug_field, "") or "").strip():
                setattr(self, slug_field, build_unique_slug(self, slug_field, title_value))

        if not (self.slug or "").strip():
            default_slug = (getattr(self, f"slug_{get_default_lang_code()}", "") or "").strip()
            if default_slug:
                self.slug = default_slug
