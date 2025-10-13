"""
Context processors para disponibilizar dados globais em todos os templates.

Este módulo fornece processadores de contexto que adicionam dados comuns
a todos os templates renderizados, evitando a necessidade de passar os
mesmos dados repetidamente em cada view.
"""

from content.models import HomePage


def home_page_settings(request):
    """
    Adiciona as configurações da HomePage ao contexto de todos os templates.
    
    Este context processor busca a primeira HomePage ativa e a disponibiliza
    globalmente, permitindo acesso a configurações como tagline do rodapé
    em qualquer template.
    
    Args:
        request (HttpRequest): Objeto de requisição HTTP do Django
        
    Returns:
        dict: Dicionário contendo:
            - home_page (HomePage|None): Instância da HomePage ou None se não existir
            
    Examples:
        No template, você pode acessar: {{ home_page.footer_tagline }}
    """
    try:
        home_page = HomePage.objects.live().first()
        return {
            'home_page': home_page,
        }
    except (HomePage.DoesNotExist, AttributeError) as e:
        # Log do erro se necessário para debugging
        # logger.warning(f"HomePage not found: {e}")
        return {
            'home_page': None,
        }
