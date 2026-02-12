"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from atadizayn_website.blog.sitemaps import BlogPostSitemap
from atadizayn_website.core.sitemaps import PolicySitemap, StaticViewSitemap
from atadizayn_website.products.sitemaps import CategorySitemap, ProductSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "policies": PolicySitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
    "blog": BlogPostSitemap,
}

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("kitchen_sink/", TemplateView.as_view(template_name="kitchen_sink.html"), name="kitchen_sink"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("blog/", include("atadizayn_website.blog.urls")),
    path("", include("atadizayn_website.core.urls")),
    path("", include("atadizayn_website.products.urls")),
)

if settings.MEDIA_STORAGE == "local":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
