from django import template
from django.utils.translation import get_language

register = template.Library()


@register.filter
def trans_field(obj, field_name: str):
	if obj is None or not field_name:
		return ""

	language = (get_language() or "").lower()
	language_base = language.split("-")[0]

	localized_field = f"{field_name}_{language}"
	localized_field_base = f"{field_name}_{language_base}"

	for candidate in (localized_field, localized_field_base, field_name):
		if hasattr(obj, candidate):
			value = getattr(obj, candidate)
			if value not in (None, ""):
				return value

	return ""
