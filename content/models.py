# Em content/models.py

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField

# SÓ PRECISAMOS DO FieldPanel AGORA
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    body = RichTextField(blank=True, verbose_name="Corpo da Página")

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

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

    # AQUI ESTÁ A MUDANÇA PRINCIPAL
    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('introduction'),
        FieldPanel('is_premium'),
        # Usamos o FieldPanel padrão para o campo de imagem. O Wagtail faz o resto.
        FieldPanel('featured_image'), 
        FieldPanel('body'),
    ]