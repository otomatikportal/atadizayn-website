from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from .models import BlogPost


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return BlogPost.objects.filter(status="published", publish_date__lte=timezone.now()).order_by("pk")

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at
