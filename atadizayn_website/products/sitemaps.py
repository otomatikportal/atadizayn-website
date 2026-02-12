from django.contrib.sitemaps import Sitemap

from .models import Category, Product


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return Category.objects.all().order_by("pk")

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return Product.objects.select_related("category").all().order_by("pk")

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at
