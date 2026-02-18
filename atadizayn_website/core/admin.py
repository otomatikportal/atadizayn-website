import re
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html, format_html_join
from modeltranslation.admin import TranslationAdmin

from .models import BrandCarouselImage, SiteAsset, SiteConfiguration


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(TranslationAdmin):
    list_display = ("key", "value", "description", "config_status", "usage_locations")
    search_fields = ("key", "value", "description")

    GET_CONFIG_PATTERN = re.compile(
        r"{%\s*get_config\s+[\"'](?P<key>[^\"']+)[\"']",
        re.IGNORECASE,
    )

    def changelist_view(self, request, extra_context=None):
        usage_map = self._collect_template_config_usage()
        self._usage_map_cache = usage_map

        used_keys = set(usage_map.keys())
        existing_keys = set(SiteConfiguration.objects.values_list("key", flat=True))
        missing_keys = sorted(used_keys - existing_keys)

        if missing_keys:
            rows = []
            for key in missing_keys:
                locations = ", ".join(usage_map.get(key, []))
                rows.append((key, locations or "Bilinmiyor"))

            msg = format_html(
                "<strong>Şablonlarda kullanılan ancak eksik olan site konfigürasyon anahtarları:</strong>"
                "<ul>{}</ul>",
                format_html_join(
                    "",
                    "<li><strong>{}</strong> → {}</li>",
                    rows,
                ),
            )
            self.message_user(request, msg, level="WARNING")

        return super().changelist_view(request, extra_context=extra_context)

    def config_status(self, obj):
        usage_map = self._get_usage_map()
        if obj.key in usage_map:
            return "✅ Kullanılıyor"
        return "➖ Şablonda kullanılmıyor"

    config_status.short_description = "Durum"

    def usage_locations(self, obj):
        usage_map = self._get_usage_map()
        locations = usage_map.get(obj.key, [])
        if not locations:
            return "-"
        return ", ".join(locations)

    usage_locations.short_description = "Kullanıldığı yerler"

    def _get_usage_map(self):
        return getattr(self, "_usage_map_cache", self._collect_template_config_usage())

    def _collect_template_config_usage(self):
        templates_dir = Path(settings.BASE_DIR) / "templates"
        usage_map = {}

        if not templates_dir.exists():
            return usage_map

        for file_path in templates_dir.rglob("*.html"):
            try:
                content = file_path.read_text(encoding="utf-8")
            except OSError:
                continue

            relative_path = file_path.relative_to(settings.BASE_DIR).as_posix()
            for line_number, line in enumerate(content.splitlines(), start=1):
                for match in self.GET_CONFIG_PATTERN.finditer(line):
                    key = match.group("key").strip()
                    if not key:
                        continue
                    location = f"{relative_path}:{line_number}"
                    existing_locations = usage_map.setdefault(key, [])
                    if location not in existing_locations:
                        existing_locations.append(location)

        for key, locations in usage_map.items():
            locations.sort()

        return usage_map


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
        ("landing_video", "Ana sayfa kahraman videosu (mp4)"),
        ("stands_banner", "Ana sayfa stand kart görseli (1:1 kare)"),
        ("fixings_banner", "Ana sayfa parça kart görseli (1:1 kare)"),
        ("part_index_banner_desktop", "Parça koleksiyonu kahraman görseli masaüstü (16:9/21:9)"),
        ("part_index_banner_mobile", "Parça koleksiyonu kahraman görseli mobil (1:1)"),
        ("stand_index_banner_desktop", "Stand koleksiyonu kahraman görseli masaüstü (16:9/21:9)"),
        ("stand_index_banner_mobile", "Stand koleksiyonu kahraman görseli mobil (1:1)"),
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
                "<strong>Şablonlarda gerekli olup eksik olan site varlıkları:</strong><ul>{}</ul>",
                format_html_join("", "<li><strong>{}</strong>: {}</li>", missing_assets),
            )
            self.message_user(request, msg, level="WARNING")

        return super().changelist_view(request, extra_context=extra_context)

    def preview_file(self, obj):
        if obj.file:
            return "✅ Yüklü"
        return "❌ Eksik"

    preview_file.short_description = "Durum"


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
