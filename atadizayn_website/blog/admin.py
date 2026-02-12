from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin):
    list_display = ("status", "collection", "title", "publish_date", "cover_preview")
    list_filter = ("status", "collection", "publish_date", "created_at")
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
            "fields": ("status", "collection", "publish_date"),
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

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "cover_image" and formfield and formfield.widget:
            formfield.widget.attrs.update(
                {
                    "data-crop-aspect": "3/1",
                    "data-crop-width": "1800",
                    "data-crop-height": "600",
                    "data-crop-title": _("Görseli Kırp (3:1)"),
                }
            )
        return formfield

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
