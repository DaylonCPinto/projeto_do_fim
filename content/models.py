# Em content/models.py

from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class HomePage(Page):
    body = RichTextField(blank=True, verbose_name="Corpo da Página")

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    # --- INÍCIO DA ALTERAÇÃO ---
    # Este método agora separa o artigo mais recente dos demais e inclui vídeos.
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Busca todos os artigos descendentes, ordenados por data de publicação
        all_articles = ArticlePage.objects.descendant_of(self).live().order_by('-publication_date')

        # O primeiro e mais recente artigo é o nosso destaque
        context['featured_article'] = all_articles.first()

        # O resto dos artigos (do segundo em diante) vai para a grade
        context['articles'] = all_articles[1:]
        
        # Busca vídeos curtos destacados
        context['featured_videos'] = VideoShort.objects.filter(is_featured=True)[:4]
        
        # Busca customizações do site
        try:
            context['site_customization'] = SiteCustomization.objects.first()
        except:
            context['site_customization'] = None

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
    
    # Opção para imagem externa via URL
    external_image_url = models.URLField(
        blank=True,
        verbose_name="URL de Imagem Externa",
        help_text="Use uma URL de imagem externa para economizar espaço. Se preenchido, será usado ao invés da imagem local."
    )

    body = RichTextField(blank=True, verbose_name="Corpo do Artigo")
    
    # Tags para categorização
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('introduction'),
        FieldPanel('is_premium'),
        MultiFieldPanel([
            FieldPanel('featured_image'),
            FieldPanel('external_image_url'),
        ], heading="Imagem de Destaque (escolha uma opção)"),
        FieldPanel('body'),
        FieldPanel('tags'),
    ]
    
    def get_image_url(self):
        """Retorna a URL da imagem, priorizando a externa"""
        if self.external_image_url:
            return self.external_image_url
        elif self.featured_image:
            return self.featured_image.file.url
        return None


@register_snippet
class VideoShort(models.Model):
    """Modelo para vídeos curtos (shorts)"""
    title = models.CharField(max_length=100, verbose_name="Título do Vídeo")
    description = models.TextField(max_length=250, blank=True, verbose_name="Descrição")
    
    # Opções de vídeo
    video_url = models.URLField(
        verbose_name="URL do Vídeo",
        help_text="URL do vídeo (YouTube, Vimeo, etc.)"
    )
    
    thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Thumbnail (Imagem de Capa)"
    )
    
    thumbnail_url = models.URLField(
        blank=True,
        verbose_name="URL do Thumbnail",
        help_text="URL externa para o thumbnail. Se preenchido, será usado ao invés da imagem local."
    )
    
    duration = models.CharField(
        max_length=10,
        default="0:30",
        verbose_name="Duração",
        help_text="Formato: M:SS (ex: 1:30)"
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Destacar na Home?",
        help_text="Vídeos destacados aparecem na seção de vídeos da home"
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name="Ordem",
        help_text="Ordem de exibição (menor número aparece primeiro)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('video_url'),
        MultiFieldPanel([
            FieldPanel('thumbnail_image'),
            FieldPanel('thumbnail_url'),
        ], heading="Thumbnail (escolha uma opção)"),
        FieldPanel('duration'),
        FieldPanel('is_featured'),
        FieldPanel('order'),
    ]
    
    class Meta:
        verbose_name = "Vídeo Curto"
        verbose_name_plural = "Vídeos Curtos"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_thumbnail_url(self):
        """Retorna a URL do thumbnail, priorizando a externa"""
        if self.thumbnail_url:
            return self.thumbnail_url
        elif self.thumbnail_image:
            return self.thumbnail_image.file.url
        return 'https://via.placeholder.com/400x700/E3120B/FFFFFF?text=Video'


@register_snippet
class SiteCustomization(models.Model):
    """Configurações de customização do site"""
    
    # Fontes
    heading_font = models.CharField(
        max_length=100,
        default="Roboto",
        verbose_name="Fonte dos Títulos",
        help_text="Nome da fonte do Google Fonts (ex: Roboto, Montserrat, Playfair Display)"
    )
    
    body_font = models.CharField(
        max_length=100,
        default="Merriweather",
        verbose_name="Fonte do Corpo",
        help_text="Nome da fonte do Google Fonts (ex: Merriweather, Open Sans, Lora)"
    )
    
    # Cores
    primary_color = models.CharField(
        max_length=7,
        default="#E3120B",
        verbose_name="Cor Primária",
        help_text="Cor principal do site (formato hexadecimal: #E3120B)"
    )
    
    secondary_color = models.CharField(
        max_length=7,
        default="#111111",
        verbose_name="Cor Secundária",
        help_text="Cor secundária (formato hexadecimal)"
    )
    
    # Layout
    show_video_section = models.BooleanField(
        default=True,
        verbose_name="Mostrar Seção de Vídeos?",
        help_text="Ativa/desativa a seção de vídeos curtos na home"
    )
    
    articles_per_page = models.IntegerField(
        default=9,
        verbose_name="Artigos por Página",
        help_text="Número de artigos a exibir na página inicial"
    )
    
    panels = [
        MultiFieldPanel([
            FieldPanel('heading_font'),
            FieldPanel('body_font'),
        ], heading="Fontes"),
        MultiFieldPanel([
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
        ], heading="Cores"),
        MultiFieldPanel([
            FieldPanel('show_video_section'),
            FieldPanel('articles_per_page'),
        ], heading="Layout"),
    ]
    
    class Meta:
        verbose_name = "Customização do Site"
        verbose_name_plural = "Customização do Site"
    
    def __str__(self):
        return "Configurações de Customização do Site"
