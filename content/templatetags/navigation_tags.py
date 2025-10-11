# content/templatetags/navigation_tags.py

from django import template
from django.apps import apps 
from django.utils import timezone
from datetime import datetime
import zoneinfo

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

@register.filter
def timesince_brasilia(value):
    """
    Calcula o tempo decorrido desde a data fornecida, 
    considerando o timezone de Brasília (America/Sao_Paulo).
    """
    if not value:
        return ''
    
    # Se for um DateField, converte para datetime no início do dia
    if isinstance(value, datetime):
        date_obj = value
    else:
        # É uma date, converte para datetime
        date_obj = datetime.combine(value, datetime.min.time())
    
    # Define o timezone de Brasília usando zoneinfo (Python 3.9+)
    try:
        brasilia_tz = zoneinfo.ZoneInfo('America/Sao_Paulo')
    except:
        # Fallback para UTC se houver problema
        brasilia_tz = zoneinfo.ZoneInfo('UTC')
    
    # Se a data não tem timezone, assume que está em Brasília
    if timezone.is_naive(date_obj):
        date_obj = date_obj.replace(tzinfo=brasilia_tz)
    
    # Obtém a data/hora atual em Brasília
    now_brasilia = timezone.now().astimezone(brasilia_tz)
    
    # Calcula a diferença
    diff = now_brasilia - date_obj
    
    if diff.days == 0:
        hours = diff.seconds // 3600
        if hours == 0:
            minutes = diff.seconds // 60
            if minutes == 0:
                return 'agora'
            return f'{minutes} minuto{"s" if minutes > 1 else ""}'
        return f'{hours} hora{"s" if hours > 1 else ""}'
    elif diff.days == 1:
        return '1 dia'
    elif diff.days < 30:
        return f'{diff.days} dias'
    elif diff.days < 365:
        months = diff.days // 30
        return f'{months} {"mês" if months == 1 else "meses"}'
    else:
        years = diff.days // 365
        return f'{years} ano{"s" if years > 1 else ""}'