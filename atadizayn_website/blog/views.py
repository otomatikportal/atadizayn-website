from django.utils import timezone
from django.views.generic import DetailView

from atadizayn_website.core.slug_utils import build_active_language_slug_lookup_q

from .models import BlogPost


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
