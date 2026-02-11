from .models import Policy


def active_policies(request):
    """Context processor to provide active policies to all templates (e.g., for footer)"""
    return {
        "active_policies": Policy.objects.filter(is_active=True)
    }
