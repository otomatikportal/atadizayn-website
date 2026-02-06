from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
	COLLECTION_CHOICES = [
		("stand", _("Standlar")),
		("part", _("Parçalar")),
	]

	name = models.CharField(
		max_length=255,
		verbose_name=_("Ad"),
	)
	slug = models.SlugField(
		max_length=255,
		blank=True,
		unique=True,
		verbose_name=_("Slug (url uç kısmı)"),
	)
	collection = models.CharField(
		max_length=10,
		choices=COLLECTION_CHOICES,
		verbose_name=_("Koleksiyon"),
	)
	description = models.TextField(
		blank=True,
		verbose_name=_("Açıklama"),
	)
	rich_text = models.TextField(
		blank=True,
		verbose_name=_("Zengin metin"),
	)
	seo_canonical = models.URLField(
		blank=True,
		default="",
		editable=False,
		verbose_name=_("Kanonik URL"),
	)
	publish_date = models.DateField(
		default=timezone.localdate,
		verbose_name=_("Yayım tarihi"),
	)

	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma tarihi"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme tarihi"))

	class Meta:
		ordering = ["name"]
		verbose_name = _("Kategori")
		verbose_name_plural = _("Kategoriler")

	def save(self, *args, **kwargs):
		english_name = (getattr(self, "name_en", None) or "").strip()
		if not english_name:
			english_name = self.name
		if not self.slug:
			self.slug = slugify(english_name, allow_unicode=True)
		super().save(*args, **kwargs)
		canonical_url = self.get_absolute_url()
		type(self).objects.filter(pk=self.pk).update(seo_canonical=canonical_url)
		self.seo_canonical = canonical_url

	def __str__(self) -> str:
		return self.name

	def get_absolute_url(self) -> str:
		return reverse("category-detail", kwargs={"category_slug": self.slug})

	def get_canonical_url(self) -> str:
		return self.seo_canonical or self.get_absolute_url()

	def clean(self):
		super().clean()
		english_name = (getattr(self, "name_en", None) or "").strip()
		if not english_name:
			raise ValidationError({"name_en": _("İngilizce ad zorunludur.")})



class Product(models.Model):
	category = models.ForeignKey(
		Category,
		on_delete=models.PROTECT,
		related_name="products",
		verbose_name=_("Kategori"),
	)
	name = models.CharField(
		max_length=255,
		verbose_name=_("Ad"),
	)
	code = models.CharField(
		max_length=100,
		unique=True,
		verbose_name=_("Kod"),
	)
	slug = models.SlugField(
		max_length=100,
		blank=True,
		editable=False,
	)
	size = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Ölçü"),
	)
	min_size = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Minimum ölçü"),
	)
	max_size = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Maksimum ölçü"),
	)
	color = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Renk"),
	)
	package_weight = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Paket ağırlığı"),
	)
	package_size = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Paket ölçüsü"),
	)
	package_quantity = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Paket içi adet"),
	)
	minimum_order = models.CharField(
		max_length=100,
		blank=True,
		verbose_name=_("Minimum sipariş"),
	)
	publish_date = models.DateField(
		default=timezone.localdate,
		verbose_name=_("Yayım tarihi"),
	)
	description = models.TextField(
		blank=True,
		verbose_name=_("Açıklama"),
	)
	rich_text = models.TextField(
		blank=True,
		verbose_name=_("Zengin metin"),
	)

	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma tarihi"))
	updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Güncellenme tarihi"))

	class Meta:
		ordering = ["name"]
		verbose_name = _("Ürün")
		verbose_name_plural = _("Ürünler")

	def clean(self):
		super().clean()
		english_name = (getattr(self, "name_en", None) or "").strip()
		if not english_name:
			raise ValidationError({"name_en": _("İngilizce ad zorunludur.")})

	def save(self, *args, **kwargs):
		if self.code:
			self.slug = slugify(self.code, allow_unicode=True)
		super().save(*args, **kwargs)

	def __str__(self) -> str:
		return self.name

	def get_absolute_url(self) -> str:
		return reverse(
			"product-detail",
			kwargs={
				"category_slug": self.category.slug,
				"product_code": self.slug,
			},
		)

	def get_canonical_url(self) -> str:
		return self.get_absolute_url()


class CategoryImage(models.Model):
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
		related_name="images",
		verbose_name=_("Kategori"),
		help_text=_("Örnek: Dizüstü Bilgisayar görsel grubu."),
	)
	image = models.ImageField(
		upload_to="categories/images/",
		verbose_name=_("Görsel"),
		help_text=_("Kategoriye ait görseli yükleyin; örn. Dizüstü bilgisayar ürün fotoğrafı."),
	)
	alt_text = models.CharField(
		max_length=255,
		blank=True,
		verbose_name=_("Alternatif metin"),
		help_text=_("Erişilebilirlik metni. Örnek: 'Dizüstü bilgisayar ön görünüm'."),
	)
	is_primary = models.BooleanField(
		default=False,
		verbose_name=_("Birincil"),
		help_text=_("Ana görsel olarak kullanılsın mı? Dizüstü bilgisayar vitrini için işaretleyin."),
	)
	sort_order = models.PositiveIntegerField(
		default=0,
		verbose_name=_("Sıralama"),
		help_text=_("Düşük sayılar ilk gösterilir. Dizüstü bilgisayar kapak görseli için 0 girin."),
	)

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Kategori görseli")
		verbose_name_plural = _("Kategori görselleri")

	def __str__(self) -> str:
		return f"{self.category.name} görseli"


class CategoryDocument(models.Model):
	category = models.ForeignKey(
		Category,
		on_delete=models.CASCADE,
		related_name="documents",
		verbose_name=_("Kategori"),
		help_text=_("Örnek: Dizüstü bilgisayar kategori kataloğu."),
	)
	title = models.CharField(
		max_length=255,
		blank=True,
		verbose_name=_("Başlık"),
		help_text=_("Belge başlığı. Örnek: 'Dizüstü Bilgisayar Teknik Kılavuzu'."),
	)
	file = models.FileField(
		upload_to="categories/documents/",
		verbose_name=_("Dosya"),
		help_text=_("PDF, katalog vb. Örnek: Dizüstü bilgisayar PDF kataloğu."),
	)
	sort_order = models.PositiveIntegerField(
		default=0,
		verbose_name=_("Sıralama"),
		help_text=_("Belge sırası; 0 dizüstü bilgisayar kataloğunu en üstte tutar."),
	)

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Kategori dokümanı")
		verbose_name_plural = _("Kategori dokümanları")

	def __str__(self) -> str:
		return self.title or f"{self.category.name} dokümanı"


class ProductImage(models.Model):
	product = models.ForeignKey(
		Product,
		on_delete=models.CASCADE,
		related_name="images",
		verbose_name=_("Ürün"),
		help_text=_("Örnek: Dizüstü Bilgisayar Pro 15 için galeri."),
	)
	image = models.ImageField(
		upload_to="products/images/",
		verbose_name=_("Görsel"),
		help_text=_("Ürün görselini yükleyin; örn. Dizüstü bilgisayar açık ekran."),
	)
	alt_text = models.CharField(
		max_length=255,
		blank=True,
		verbose_name=_("Alternatif metin"),
		help_text=_("Örnek: 'Dizüstü Bilgisayar Pro 15 üstten görünüm'."),
	)
	is_primary = models.BooleanField(
		default=False,
		verbose_name=_("Birincil"),
		help_text=_("Ürün kartlarında kullanılacak ana görseli işaretleyin."),
	)
	sort_order = models.PositiveIntegerField(
		default=0,
		verbose_name=_("Sıralama"),
		help_text=_("Galeri sırası; 0 değerini Dizüstü bilgisayar kapak fotoğrafı için kullanın."),
	)

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Ürün görseli")
		verbose_name_plural = _("Ürün görselleri")

	def __str__(self) -> str:
		return f"{self.product.name} görseli"


class ProductDocument(models.Model):
	product = models.ForeignKey(
		Product,
		on_delete=models.CASCADE,
		related_name="documents",
		verbose_name=_("Ürün"),
		help_text=_("Örnek: Dizüstü Bilgisayar Pro 15 kullanım kılavuzu."),
	)
	title = models.CharField(
		max_length=255,
		blank=True,
		verbose_name=_("Başlık"),
		help_text=_("Belge adı. Örnek: 'Dizüstü Bilgisayar Pro 15 PDF'."),
	)
	file = models.FileField(
		upload_to="products/documents/",
		verbose_name=_("Dosya"),
		help_text=_("Teknik föy, kullanım kılavuzu vb."),
	)
	sort_order = models.PositiveIntegerField(
		default=0,
		verbose_name=_("Sıralama"),
		help_text=_("Belge gösterim sırası."),
	)

	class Meta:
		ordering = ["sort_order", "id"]
		verbose_name = _("Ürün dokümanı")
		verbose_name_plural = _("Ürün dokümanları")

	def __str__(self) -> str:
		return self.title or f"{self.product.name} dokümanı"
