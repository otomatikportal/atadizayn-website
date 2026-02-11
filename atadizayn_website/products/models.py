from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    COLLECTION_CHOICES = [
        ("stand", _("Standlar")),
        ("part", _("Parçalar")),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name=_("Ad"),
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        unique=True,
        verbose_name=_("Slug (url uç kısmı)"),
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

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Oluşturulma tarihi")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Güncellenme tarihi")
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Kategori")
        verbose_name_plural = _("Kategoriler")

    def save(self, *args, **kwargs):
        # Auto-generate slug from default language name if not set
        if not self.slug and self.name:
            self.slug = slugify(self.name, allow_unicode=False)

        super().save(*args, **kwargs)

        # Canonical URL logic (usually points to default language)
        canonical_url = self.get_absolute_url()
        type(self).objects.filter(pk=self.pk).update(seo_canonical=canonical_url)
        self.seo_canonical = canonical_url

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("category-detail", kwargs={"category_slug": self.slug})

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


class Product(models.Model):
    category = models.ForeignKey(
        Category,
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
        unique=True, # Recommended to add unique=True if using name-based slugs
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

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Oluşturulma tarihi")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Güncellenme tarihi")
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Ürün")
        verbose_name_plural = _("Ürünler")

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

    def save(self, *args, **kwargs):
        # Auto-generate slug from default language name if not set
        if not self.slug and self.name:
            self.slug = slugify(self.name, allow_unicode=False)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse(
            "product-detail",
            kwargs={
                "category_slug": self.category.slug,
                "product_code": self.slug,
            },
        )


class CategoryImage(models.Model):
    category = models.ForeignKey(
        Category,
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


class CategoryDocument(models.Model):
    category = models.ForeignKey(
        Category,
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


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
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


class ProductDocument(models.Model):
    product = models.ForeignKey(
        Product,
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
        Product,
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

    def get_absolute_url(self):
        return self.product.get_absolute_url()
