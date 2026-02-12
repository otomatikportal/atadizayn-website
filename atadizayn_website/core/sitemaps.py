from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return ["home", "part_index", "stand_index", "blog-index", "blog-announcements", "blog-policies", "blog-corporate"]

    def location(self, item):
        return reverse(item)
