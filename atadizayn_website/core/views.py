from django.shortcuts import render

from atadizayn_website.core.models import BrandCarouselImage
from atadizayn_website.products.models import Category


def home(request):
	categories = list(Category.objects.order_by("name").prefetch_related("images"))
	carousel_categories = []
	for category in categories:
		images = list(category.images.all())
		if not images:
			continue
		category.carousel_image = images[0]
		carousel_categories.append(category)
		if len(carousel_categories) >= 3:
			break
	
	# Get brand carousel images
	brands = BrandCarouselImage.objects.filter(is_active=True)
	
	context = {
		"categories": categories,
		"carousel_categories": carousel_categories,
		"brands": brands,
	}
	return render(request, "home.html", context)