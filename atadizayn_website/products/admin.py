from django.contrib import admin
from .models import (
	Category,
	Product,
	CategoryImage,
	CategoryDocument,
	ProductImage,
	ProductDocument,
)


class CategoryImageInline(admin.TabularInline):
	model = CategoryImage
	extra = 1


class CategoryDocumentInline(admin.TabularInline):
	model = CategoryDocument
	extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name", "slug", "collection", "publish_date"]
	prepopulated_fields = {"slug": ("name",)}
	inlines = [CategoryImageInline, CategoryDocumentInline]


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


class ProductDocumentInline(admin.TabularInline):
	model = ProductDocument
	extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ["name", "code", "category", "publish_date"]
	inlines = [ProductImageInline, ProductDocumentInline]


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
	list_display = ["category", "is_primary", "sort_order"]


@admin.register(CategoryDocument)
class CategoryDocumentAdmin(admin.ModelAdmin):
	list_display = ["category", "title", "sort_order"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ["product", "is_primary", "sort_order"]


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
	list_display = ["product", "title", "sort_order"]
