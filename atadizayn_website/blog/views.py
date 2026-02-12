from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language
from django.views.generic import DetailView

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
        lang_code = (get_language() or "").split("-")[0] or "tr"
        language_slug_field = f"slug_{lang_code}"

        return queryset.get(
            Q(slug=slug)
            | Q(slug_en=slug)
            | Q(slug_tr=slug)
            | Q(**{language_slug_field: slug})
        )
