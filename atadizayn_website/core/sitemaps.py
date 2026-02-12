from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Policy


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return ["home", "part_index", "stand_index"]

    def location(self, item):
        return reverse(item)


class PolicySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return Policy.objects.filter(is_active=True).order_by("pk")

    def location(self, obj):
        return reverse("policy_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.updated_at
