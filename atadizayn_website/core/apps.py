from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "atadizayn_website.core"
    verbose_name = _("Temel Özellikler")
