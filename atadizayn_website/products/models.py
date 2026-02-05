from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
	name = models.CharField(max_length=255, verbose_name=_("Name"))
	slug = models.SlugField(max_length=255, blank=True, unique=True, verbose_name=_("Slug"))
	description = models.TextField(blank=True, verbose_name=_("Description"))
	rich_text = models.TextField(blank=True, verbose_name=_("Rich text"))
	seo_title = models.CharField(max_length=255, blank=True, verbose_name=_("SEO title"))
	seo_description = models.CharField(max_length=500, blank=True, verbose_name=_("SEO description"))

	parent = TreeForeignKey(
		"self",
		on_delete=models.CASCADE,
		null=True,
		blank=True,
		related_name="children",
		verbose_name=_("Parent"),
	)

	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

	class MPTTMeta:
		order_insertion_by = ["name"]

	class Meta:
		ordering = ["name"]
		verbose_name = _("Category")
		verbose_name_plural = _("Categories")
		constraints = [
			models.UniqueConstraint(fields=["parent", "slug"], name="unique_category_slug_per_parent"),
		]

	def save(self, *args, **kwargs):
		if not self.slug:
			base_name = getattr(self, "name_tr", None) or self.name
			self.slug = slugify(base_name, allow_unicode=True)
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return self.name

	def get_path(self) -> str:
		segments = [node.slug for node in self.get_ancestors(include_self=True)]
		return "/".join(segments)

	def get_absolute_url(self) -> str:
		return reverse("products:category-detail", kwargs={"category_path": self.get_path()})



class Product(models.Model):
	category = models.ForeignKey(
		Category,
		on_delete=models.PROTECT,
		related_name="products",
		verbose_name=_("Category"),
	)
	name = models.CharField(max_length=255, verbose_name=_("Name"))
	code = models.SlugField(max_length=100, unique=True, verbose_name=_("Code"))
	size = models.CharField(max_length=100, blank=True, verbose_name=_("Size"))
	min_size = models.CharField(max_length=100, blank=True, verbose_name=_("Min size"))
	max_size = models.CharField(max_length=100, blank=True, verbose_name=_("Max size"))
	color = models.CharField(max_length=100, blank=True, verbose_name=_("Color"))
	weight = models.CharField(max_length=100, blank=True, verbose_name=_("Ağırlık"))
	package_size = models.CharField(max_length=100, blank=True, verbose_name=_("Paket ölçüsü"))
	package_quantity = models.CharField(max_length=100, blank=True, verbose_name=_("Paket içi adet"))
	minimum_order = models.CharField(max_length=100, blank=True, verbose_name=_("Minimum sipariş"))
	description = models.TextField(blank=True, verbose_name=_("Description"))
	rich_text = models.TextField(blank=True, verbose_name=_("Rich text"))
	seo_title = models.CharField(max_length=255, blank=True, verbose_name=_("SEO title"))
	seo_description = models.CharField(max_length=500, blank=True, verbose_name=_("SEO description"))

	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

	class Meta:
		ordering = ["name"]
		verbose_name = _("Product")
		verbose_name_plural = _("Products")

	def clean(self):
		super().clean()
		if self.category and not self.category.is_leaf_node():
			raise ValidationError({"category": _("Products can only be assigned to leaf categories.")})

	def save(self, *args, **kwargs):
		if self.code:
			self.code = slugify(self.code, allow_unicode=True)
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return self.name

	def get_absolute_url(self) -> str:
		return reverse(
			"products:product-detail",
			kwargs={
				"category_path": self.category.get_path(),
				"product_code": self.code,
			},
		)


class CategoryImage(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="images", verbose_name=_("Category"))
	image = models.ImageField(upload_to="categories/images/", verbose_name=_("Image"))
	alt_text = models.CharField(max_length=255, blank=True, verbose_name=_("Alt text"))
	is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
	sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Category image")
		verbose_name_plural = _("Category images")

	def __str__(self) -> str:
		return f"{self.category.name} görsel"


class CategoryDocument(models.Model):
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
		related_name="documents",
		verbose_name=_("Category"),
	)
	title = models.CharField(max_length=255, blank=True, verbose_name=_("Title"))
	file = models.FileField(upload_to="categories/documents/", verbose_name=_("File"))
	sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Category document")
		verbose_name_plural = _("Category documents")

	def __str__(self) -> str:
		return self.title or f"{self.category.name} dosya"


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name=_("Product"))
	image = models.ImageField(upload_to="products/images/", verbose_name=_("Image"))
	alt_text = models.CharField(max_length=255, blank=True, verbose_name=_("Alt text"))
	is_primary = models.BooleanField(default=False, verbose_name=_("Is primary"))
	sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Product image")
		verbose_name_plural = _("Product images")

	def __str__(self) -> str:
		return f"{self.product.name} تصویر"


class ProductDocument(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="documents", verbose_name=_("Product"))
	title = models.CharField(max_length=255, blank=True, verbose_name=_("Title"))
	file = models.FileField(upload_to="products/documents/", verbose_name=_("File"))
	sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Product document")
		verbose_name_plural = _("Product documents")

	def __str__(self) -> str:
		return self.title or f"{self.product.name} فایل"
