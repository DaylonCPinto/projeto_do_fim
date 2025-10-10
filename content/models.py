# Em content/models.py

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

# Em content/models.py

# ... (suas importações no topo do arquivo continuam iguais) ...

class HomePage(Page):
    body = RichTextField(blank=True, verbose_name="Corpo da Página")

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    # O método get_context DEVE estar indentado para pertencer à classe
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Usando a versão SIMPLES que sabemos que funciona
        all_articles = ArticlePage.objects.descendant_of(self).live().order_by('-publication_date')
        context['articles'] = all_articles

        return context


class ArticlePage(Page):
    publication_date = models.DateField(verbose_name="Data de Publicação")
    introduction = models.CharField(max_length=250, verbose_name="Introdução")
    is_premium = models.BooleanField(default=False, verbose_name="Conteúdo Exclusivo?")
    
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem de Destaque"
    )

    body = RichTextField(blank=True, verbose_name="Corpo do Artigo")

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('introduction'),
        FieldPanel('is_premium'),
        FieldPanel('featured_image'), 
        FieldPanel('body'),
    ]