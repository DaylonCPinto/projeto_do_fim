"""Context processors compartilhados entre os templates do projeto."""

from content.models import HomePage


def home_page_settings(request):
    """Disponibiliza a primeira HomePage publicada para todos os templates."""
    try:
        home_page = HomePage.objects.live().first()
        return {
            'home_page': home_page,
        }
    except (HomePage.DoesNotExist, AttributeError):
        return {
            'home_page': None,
        }
