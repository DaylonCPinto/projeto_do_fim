# Em content/templatetags/navigation_tags.py

from django import template
from content.models import TopicListingPage

register = template.Library()

@register.simple_tag()
def get_topics():
    # Esta tag busca todas as páginas de tópico publicadas para usar no menu
    return TopicListingPage.objects.live().order_by('title')
