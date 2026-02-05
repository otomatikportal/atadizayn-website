from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from mptt.admin import MPTTModelAdmin

from .models import (
	Category,
	CategoryDocument,
	CategoryImage,
	Product,
	ProductDocument,
	ProductImage,
)


class CategoryImageInline(admin.TabularInline):
	model = CategoryImage
	extra = 1


class CategoryDocumentInline(admin.TabularInline):
	model = CategoryDocument
	extra = 1


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, MPTTModelAdmin):
	list_display = ("name", "parent", "updated_at")
	search_fields = ("name", "slug")
	inlines = [CategoryImageInline, CategoryDocumentInline]
	prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


class ProductDocumentInline(admin.TabularInline):
	model = ProductDocument
	extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
	list_display = ("name", "code", "category", "updated_at")
	search_fields = ("name", "code")
	list_filter = ("updated_at",)
	inlines = [ProductImageInline, ProductDocumentInline]
	prepopulated_fields = {"code": ("name",)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ("product", "is_primary", "sort_order")
	list_filter = ("is_primary",)


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
	list_display = ("product", "title", "sort_order")
