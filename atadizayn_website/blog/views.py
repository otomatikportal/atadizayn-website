from django.utils import timezone
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _

from atadizayn_website.core.slug_utils import build_active_language_slug_lookup_q

from .models import BlogPost


COLLECTION_LABELS = {
    "policy": _("Politikalar"),
    "announcement": _("Duyurular"),
    "post": _("Blog paylaşımları"),
    "corporate": _("Kurumsal"),
}

COLLECTION_SUBTITLES = {
    "policy": _("Tüm politika içeriklerimizi bu sayfada bulabilirsiniz."),
    "announcement": _("En güncel duyurularımızı burada takip edebilirsiniz."),
    "post": _("Atadizayn’dan haberler, fikirler ve ürün odaklı paylaşımlar."),
    "corporate": _("Kurumsal içerik ve paylaşımlarımız."),
}


def _published_posts_queryset():
    return BlogPost.objects.filter(status="published", publish_date__lte=timezone.now()).order_by("-publish_date")


def blog_index(request):
    posts_queryset = _published_posts_queryset().filter(collection="post")
    paginator = Paginator(posts_queryset, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "blog/index.html",
        {
            "page_obj": page_obj,
            "page_title_text": COLLECTION_LABELS["post"],
            "page_subtitle_text": COLLECTION_SUBTITLES["post"],
        },
    )


def blog_collection_index(request, collection):
    if collection not in COLLECTION_LABELS:
        raise Http404

    posts_queryset = _published_posts_queryset().filter(collection=collection)
    paginator = Paginator(posts_queryset, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "blog/index.html",
        {
            "page_obj": page_obj,
            "page_title_text": COLLECTION_LABELS[collection],
            "page_subtitle_text": COLLECTION_SUBTITLES[collection],
        },
    )


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(status="published", publish_date__lte=timezone.now())

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        slug = self.kwargs["slug"]
        try:
            return queryset.get(build_active_language_slug_lookup_q(slug))
        except BlogPost.DoesNotExist:
            raise Http404(_("Blog yazısı bulunamadı."))
