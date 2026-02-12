from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "atadizayn_website.products"
    verbose_name = _("Ürün yönetimi")
