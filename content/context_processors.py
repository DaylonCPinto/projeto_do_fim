"""
Context processors para disponibilizar dados globais em todos os templates.
"""

from content.models import HomePage


def home_page_settings(request):
    """
    Adiciona as configurações da HomePage ao contexto de todos os templates.
    
    Args:
        request: HttpRequest object
        
    Returns:
        dict: Dicionário com a instância home_page
    """
    try:
        home_page = HomePage.objects.live().first()
        return {
            'home_page': home_page,
        }
    except (HomePage.DoesNotExist, AttributeError):
        return {
            'home_page': None,
        }
