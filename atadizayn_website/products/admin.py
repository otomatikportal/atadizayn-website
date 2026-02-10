from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from .models import (
    Category,
    Product,
    CategoryImage,
    CategoryDocument,
    ProductImage,
    ProductDocument,
    ProductVariant,
)

# --- Category Inlines ---

class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 1

class CategoryDocumentInline(admin.TabularInline):
    model = CategoryDocument
    extra = 1

# --- Category Admin ---

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "collection", "publish_date"]
    exclude = ["slug", "slug_en", "slug_tr", "seo_canonical"]
    inlines = [CategoryImageInline, CategoryDocumentInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    min_num = 1
    fields = ('code', 'size', 'package_weight', 'package_size', 'package_quantity', 'minimum_order')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument
    extra = 1

# --- Product Admin (Consolidated) ---

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    # 'code' is removed from list_display because it is now in the Variant
    list_display = ["name", "category", "get_variants_count", "publish_date"]
    exclude = ["slug", "slug_en", "slug_tr"]
    
    # Combined inlines: Variant + Images + Documents
    inlines = [
        ProductVariantInline,
        ProductImageInline,
        ProductDocumentInline
    ]

    def get_variants_count(self, obj):
        return obj.variants.count()
    get_variants_count.short_description = "Varyant Sayısı"

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }