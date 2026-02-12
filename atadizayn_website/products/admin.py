from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import (
    Category,
    CategoryDocument,
    CategoryImage,
    Product,
    ProductDocument,
    ProductImage,
    ProductVariant,
)

# --- Category Inlines ---


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "is_primary", "sort_order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 5px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Önizleme"


class CategoryDocumentInline(admin.TabularInline):
    model = CategoryDocument
    extra = 1


# --- Category Admin ---


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "collection", "publish_date"]
    exclude = ["seo_canonical"]
    prepopulated_fields = {
        "slug": ("name",),
        "slug_en": ("name_en",),
        "slug_tr": ("name_tr",),
    }
    inlines = [CategoryImageInline, CategoryDocumentInline]

    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
            "js/admin_crop.js",
        )
        css = {
            "screen": (
                "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css",
                "modeltranslation/css/tabbed_translation_fields.css",
            ),
            "all": ("https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.css",),
        }


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    min_num = 1
    fields = ("code", "size", "package_weight", "package_size", "package_quantity", "minimum_order")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "is_primary", "sort_order")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 5px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Önizleme"


class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument
    extra = 1


# --- Product Admin (Consolidated) ---


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    # 'code' is removed from list_display because it is now in the Variant
    list_display = ["name", "category", "get_variants_count", "publish_date"]
    prepopulated_fields = {
        "slug": ("name",),
        "slug_en": ("name_en",),
        "slug_tr": ("name_tr",),
    }

    # Combined inlines: Variant + Images + Documents
    inlines = [ProductVariantInline, ProductImageInline, ProductDocumentInline]

    def get_variants_count(self, obj):
        return obj.variants.count()

    get_variants_count.short_description = "Varyant Sayısı"

    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
            "js/admin_crop.js",
        )
        css = {
            "screen": (
                "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css",
                "modeltranslation/css/tabbed_translation_fields.css",
            ),
            "all": ("https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.css",),
        }
