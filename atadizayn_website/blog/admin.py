from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display = ("status", "title", "publish_date", "cover_preview")
    list_filter = ("status", "publish_date", "created_at")
    search_fields = ("title", "meta_description", "content")
    readonly_fields = ("created_at", "updated_at")
    radio_fields = {"status": admin.HORIZONTAL}
    prepopulated_fields = {
        "slug": ("title",),
        "slug_en": ("title_en",),
        "slug_tr": ("title_tr",),
    }

    fieldsets = (
        (_("Yayın Durumu"), {
            "fields": ("status", "publish_date"),
            "classes": ("wide",),
        }),
        (_("Temel Bilgiler & SEO"), {
            "fields": (
                "title",
                "slug",
                "meta_description",
                "cover_image",
                "cover_image_alt",
            )
        }),
        (_("İçerik"), {
            "fields": ("content",)
        }),
        (_("Sistem Kayıtları"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 3px;" />', obj.cover_image.url)
        return "-"
    cover_preview.short_description = _("Kapak")

    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": (
                "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css",
                "modeltranslation/css/tabbed_translation_fields.css",
            ),
        }
