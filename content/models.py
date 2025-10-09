# Em content/models.py

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField  # Apenas o RichTextField vem daqui
from wagtail.admin.panels import FieldPanel

class HomePage(Page):
    body = RichTextField(blank=True, verbose_name="Corpo da Página")

    content_panels = Page.content_panels + [
        FieldPanel('body'),
]
# ADICIONE ESTE MÉTODO DENTRO DA CLASSE HomePage
    def get_context(self, request):
        # Primeiro, chame o método original para obter o contexto base
        context = super().get_context(request)

        # Obtenha os artigos que são filhos desta página,
        # apenas os que estão publicados (.live()) e ordene-os
        # pela data de publicação, do mais novo para o mais antigo
        articles = ArticlePage.objects.child_of(self).live().order_by('-publication_date')

        # Adicione a lista de artigos ao contexto com a chave 'articles'
        context['articles'] = articles
        return context


class ArticlePage(Page):
    # Usamos models.DateField para indicar que é um campo padrão do Django
    publication_date = models.DateField(verbose_name="Data de Publicação")
    introduction = models.CharField(max_length=250, verbose_name="Introdução")
    is_premium = models.BooleanField(default=False, verbose_name="Conteúdo Exclusivo?")
    body = RichTextField(blank=True, verbose_name="Corpo do Artigo")

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('introduction'),
        FieldPanel('is_premium'),
        FieldPanel('body'),
    ]