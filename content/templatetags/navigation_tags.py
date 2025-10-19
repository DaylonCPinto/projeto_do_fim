# content/templatetags/navigation_tags.py

from django import template
from django.apps import apps 
from django.utils import timezone
from datetime import datetime
import zoneinfo

register = template.Library()

@register.simple_tag()
def get_topics():
    """Retorna os artigos publicados ordenados alfabeticamente."""
    ArticlePage = apps.get_model('content', 'ArticlePage')
    return ArticlePage.objects.live().order_by('title')

@register.simple_tag()
def get_support_sections():
    """Lista páginas de apoio publicadas para uso na navegação."""
    SupportSectionPage = apps.get_model('content', 'SupportSectionPage')
    return SupportSectionPage.objects.live().order_by('title')


@register.simple_tag()
def get_site_customization():
    """Retorna a configuração global do site, quando disponível."""
    SiteCustomization = apps.get_model('content', 'SiteCustomization')
    return SiteCustomization.objects.first()

@register.filter
def timesince_brasilia(value):
    """Calcula o tempo decorrido usando o fuso horário de Brasília."""
    if not value:
        return ''
    
    from datetime import date
    
    # Se for um DateField, converte para datetime no início do dia
    if isinstance(value, datetime):
        date_obj = value
    elif isinstance(value, date):
        # É uma date, converte para datetime no início do dia
        date_obj = datetime.combine(value, datetime.min.time())
    else:
        return ''
    
    # Define o timezone de Brasília usando zoneinfo (Python 3.9+)
    try:
        brasilia_tz = zoneinfo.ZoneInfo('America/Sao_Paulo')
    except:
        # Fallback para UTC se houver problema
        brasilia_tz = zoneinfo.ZoneInfo('UTC')
    
    # Se a data não tem timezone, assume que está em Brasília
    if timezone.is_naive(date_obj):
        date_obj = date_obj.replace(tzinfo=brasilia_tz)
    else:
        # Converte para o timezone de Brasília
        date_obj = date_obj.astimezone(brasilia_tz)
    
    # Obtém a data/hora atual em Brasília
    now_brasilia = timezone.now().astimezone(brasilia_tz)
    
    # Calcula a diferença
    diff = now_brasilia - date_obj
    
    # Previne diferenças negativas (datas futuras)
    if diff.total_seconds() < 0:
        return 'agora'
    
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
