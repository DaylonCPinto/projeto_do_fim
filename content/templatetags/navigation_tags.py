# content/templatetags/navigation_tags.py

from django import template
from django.apps import apps 

register = template.Library()

@register.simple_tag()
def get_topics():
    # CORREÇÃO CRÍTICA: Substituindo 'TopicPage' pelo provável nome real do modelo: 'ArticlePage'
    ArticlePage = apps.get_model('content', 'ArticlePage') # <-- TENTATIVA FINAL
    
    # A consulta deve buscar todas as páginas de ARTIGO que estão vivas.
    # No entanto, se o menu é de TÓPICOS, você precisaria de uma lógica 
    # mais complexa para pegar os TÓPICOS únicos dos artigos ou a página INDEX.
    # Mas, para resolver a LookupError, vamos buscar as páginas de Artigo:
    return ArticlePage.objects.live().order_by('title')