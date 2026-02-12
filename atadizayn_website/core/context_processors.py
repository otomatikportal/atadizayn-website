from django.utils import timezone

from atadizayn_website.blog.models import BlogPost


def footer_blog_collections(request):
    published_posts = BlogPost.objects.filter(status="published", publish_date__lte=timezone.now())
    return {
        "footer_policy_posts": published_posts.filter(collection="policy"),
        "footer_corporate_posts": published_posts.filter(collection="corporate"),
    }


def canonical_url(request):
    return {
        "canonical_url": request.build_absolute_uri(request.path),
    }
