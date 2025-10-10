# Em content/models.py

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class HomePage(Page):
    body = RichTextField(blank=True, verbose_name="Corpo da Página")

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    # --- INÍCIO DA ALTERAÇÃO ---
    # Este método agora separa o artigo mais recente dos demais.
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Busca todos os artigos descendentes, ordenados por data de publicação
        all_articles = ArticlePage.objects.descendant_of(self).live().order_by('-publication_date')

        # O primeiro e mais recente artigo é o nosso destaque
        context['featured_article'] = all_articles.first()

        # O resto dos artigos (do segundo em diante) vai para a grade
        context['articles'] = all_articles[1:]

        return context
    # --- FIM DA ALTERAÇÃO ---


class ArticlePageTag(TaggedItemBase):
    """
    Modelo intermediário para tags de artigos.
    """
    content_object = ParentalKey(
        'ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


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
    
    # Tags para categorização
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('introduction'),
        FieldPanel('is_premium'),
        FieldPanel('featured_image'), 
        FieldPanel('body'),
        FieldPanel('tags'),
    ]
