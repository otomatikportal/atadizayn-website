from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView

from atadizayn_website.core.slug_utils import build_active_language_slug_lookup_q

from .models import BlogPost


def blog_index(request):
    posts_queryset = BlogPost.objects.filter(status="published", publish_date__lte=timezone.now()).order_by("-publish_date")
    paginator = Paginator(posts_queryset, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/index.html", {"page_obj": page_obj})


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(status="published", publish_date__lte=timezone.now())

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        slug = self.kwargs["slug"]
        return queryset.get(build_active_language_slug_lookup_q(slug))
