from django.contrib import admin
from .models import BrandCarouselImage


@admin.register(BrandCarouselImage)
class BrandCarouselImageAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'icon_name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('alt_text', 'icon_name')
    ordering = ('order',)
