from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from .models import BrandCarouselImage, SiteAsset, Policy, SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(TranslationAdmin):
    list_display = ("key", "value", "description")
    search_fields = ("key", "value", "description")


@admin.register(Policy)
class PolicyAdmin(TranslationAdmin):
    list_display = ("name", "slug", "order", "is_active", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order", "is_active", "updated_at")
    search_fields = ("name", "slug")


@admin.register(SiteAsset)
class SiteAssetAdmin(admin.ModelAdmin):
    list_display = ("key", "description", "file", "preview_file", "image_preview")
    search_fields = ("key", "description")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.file and any(obj.file.name.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 5px;" />', obj.file.url)
        return "-"

    image_preview.short_description = "Görsel Önizleme"

    REQUIRED_ASSETS = [
        ("landing_video", "Home Page Hero Video (mp4)"),
        ("stands_banner", "Home Page Stands Card Image (Square 1:1)"),
        ("fixings_banner", "Home Page Parts Card Image (Square 1:1)"),
        ("part_index_banner_desktop", "Part Collection Hero Desktop (16:9/21:9)"),
        ("part_index_banner_mobile", "Part Collection Hero Mobile (1:1)"),
        ("stand_index_banner_desktop", "Stand Collection Hero Desktop (16:9/21:9)"),
        ("stand_index_banner_mobile", "Stand Collection Hero Mobile (1:1)"),
    ]

    def changelist_view(self, request, extra_context=None):
        # check for missing assets
        existing_keys = set(SiteAsset.objects.values_list("key", flat=True))
        missing_assets = []
        for key, desc in self.REQUIRED_ASSETS:
            if key not in existing_keys:
                missing_assets.append((key, desc))

        if missing_assets:
            msg = format_html(
                "<strong>Warning: The following assets are required by templates but missing:</strong><ul>{}</ul>",
                format_html_join("", "<li><strong>{}</strong>: {}</li>", missing_assets),
            )
            self.message_user(request, msg, level="WARNING")

        return super().changelist_view(request, extra_context=extra_context)

    def preview_file(self, obj):
        if obj.file:
            return "✅ Uploaded"
        return "❌ Missing"

    preview_file.short_description = "Status"


@admin.register(BrandCarouselImage)
class BrandCarouselImageAdmin(admin.ModelAdmin):
    list_display = ("alt_text", "is_active", "image_preview")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("alt_text",)
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Görsel Önizleme"
