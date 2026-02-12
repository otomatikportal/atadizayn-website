from django.db import migrations, models
from django.utils.text import slugify


def _build_unique_slug(model_cls, field_name, source_text, pk):
    base_slug = slugify(source_text or "", allow_unicode=False)
    if not base_slug:
        return ""

    candidate = base_slug
    suffix = 2
    queryset = model_cls.objects.exclude(pk=pk)
    while queryset.filter(**{field_name: candidate}).exists():
        candidate = f"{base_slug}-{suffix}"
        suffix += 1
    return candidate


def forwards(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")

    for category in Category.objects.all():
        source_en = (category.name_en or category.name or "").strip()
        source_tr = (category.name_tr or category.name or "").strip()

        category.slug_en = _build_unique_slug(Category, "slug_en", source_en, category.pk) if source_en else None
        category.slug_tr = _build_unique_slug(Category, "slug_tr", source_tr, category.pk) if source_tr else None

        if category.slug_tr:
            category.slug = category.slug_tr
        elif category.slug_en:
            category.slug = category.slug_en
        elif not category.slug:
            category.slug = _build_unique_slug(Category, "slug", category.name or "category", category.pk)

        category.save(update_fields=["slug", "slug_en", "slug_tr"])

    for product in Product.objects.all():
        source_en = (product.name_en or product.name or "").strip()
        source_tr = (product.name_tr or product.name or "").strip()

        product.slug_en = _build_unique_slug(Product, "slug_en", source_en, product.pk) if source_en else None
        product.slug_tr = _build_unique_slug(Product, "slug_tr", source_tr, product.pk) if source_tr else None

        if product.slug_tr:
            product.slug = product.slug_tr
        elif product.slug_en:
            product.slug = product.slug_en
        elif not product.slug:
            product.slug = _build_unique_slug(Product, "slug", product.name or "product", product.pk)

        product.save(update_fields=["slug", "slug_en", "slug_tr"])


def backwards(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")

    Category.objects.update(slug_en=None, slug_tr=None)
    Product.objects.update(slug_en=None, slug_tr=None)


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug_en",
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name="Slug (url uç kısmı)"),
        ),
        migrations.AddField(
            model_name="category",
            name="slug_tr",
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name="Slug (url uç kısmı)"),
        ),
        migrations.AddField(
            model_name="product",
            name="slug_en",
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name="Slug"),
        ),
        migrations.AddField(
            model_name="product",
            name="slug_tr",
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name="Slug"),
        ),
        migrations.RunPython(forwards, backwards),
    ]
