# Em content/models.py

from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


# Custom block for images with URL support
class ImageBlock(blocks.StructBlock):
    """Block that supports both uploaded images and external URLs"""
    image = ImageChooserBlock(
        required=False,
        label="Imagem (Upload)"
    )
    image_url = blocks.URLBlock(
        required=False,
        label="URL da Imagem",
        help_text="Ou use uma URL de imagem externa"
    )
    caption = blocks.CharBlock(
        required=False,
        label="Legenda"
    )
    credit = blocks.CharBlock(
        required=False,
        label="Crédito"
    )
    
    class Meta:
        icon = "image"
        label = "Imagem (Upload ou URL)"
        template = "content/blocks/image_block.html"


# Custom block for GIFs
class GifBlock(blocks.StructBlock):
    """Block for GIF animations"""
    gif_url = blocks.URLBlock(
        label="URL do GIF",
        help_text="Cole a URL do GIF (ex: de um serviço como Giphy, Tenor, ou seu próprio servidor)"
    )
    caption = blocks.CharBlock(
        required=False,
        label="Legenda"
    )
    
    class Meta:
        icon = "media"
        label = "GIF Animado"
        template = "content/blocks/gif_block.html"


# Custom block for Audio/Podcast
class AudioBlock(blocks.StructBlock):
    """Block for audio player (podcast style)"""
    audio_url = blocks.URLBlock(
        label="URL do Áudio",
        help_text="Cole a URL do arquivo de áudio (MP3, WAV, etc.)"
    )
    title = blocks.CharBlock(
        required=False,
        label="Título do Áudio"
    )
    description = blocks.TextBlock(
        required=False,
        label="Descrição"
    )
    
    class Meta:
        icon = "media"
        label = "Áudio/Podcast"
        template = "content/blocks/audio_block.html"


# Custom block for PDF Download
class PDFDownloadBlock(blocks.StructBlock):
    """Block for PDF download with icon"""
    pdf_url = blocks.URLBlock(
        label="URL do PDF",
        help_text="Cole a URL do arquivo PDF para download"
    )
    title = blocks.CharBlock(
        label="Título do Documento",
        default="Baixar PDF"
    )
    description = blocks.CharBlock(
        required=False,
        label="Descrição",
        help_text="Descrição opcional do documento"
    )
    
    class Meta:
        icon = "doc-full"
        label = "Download PDF"
        template = "content/blocks/pdf_block.html"

class HomePage(Page):
    body = RichTextField(blank=True, verbose_name="Corpo da Página")

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    
    # Define what types of pages can be children of HomePage
    subpage_types = ['content.SectionPage', 'content.ArticlePage', 'content.VideosPage']

    # --- INÍCIO DA ALTERAÇÃO ---
    # Este método agora separa o artigo mais recente dos demais e inclui vídeos.
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Busca todos os artigos descendentes
        all_articles = ArticlePage.objects.descendant_of(self).live()
        
        # Prioriza artigos marcados como "Alto Impacto" para o destaque
        featured_highlight = all_articles.filter(is_featured_highlight=True).order_by('-publication_date').first()
        
        if featured_highlight:
            # Se existe um artigo de alto impacto, ele é o destaque
            context['featured_article'] = featured_highlight
            # Exclui o artigo de destaque da lista de artigos
            context['articles'] = all_articles.exclude(id=featured_highlight.id).order_by('-publication_date')
        else:
            # Caso contrário, o artigo mais recente é o destaque
            all_articles_ordered = all_articles.order_by('-publication_date')
            context['featured_article'] = all_articles_ordered.first()
            context['articles'] = all_articles_ordered[1:]
        
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
    # Section choices
    SECTION_CHOICES = [
        ('em-alta', 'Em Alta'),
        ('geopolitica', 'Geopolítica'),
        ('economia', 'Economia'),
        ('clima', 'Clima'),
        ('tecnologia', 'Tecnologia'),
        ('escatologia', 'Escatologia'),
    ]
    
    publication_date = models.DateTimeField(verbose_name="Data de Publicação", default=timezone.now)
    
    # Font choices for title display
    FONT_CHOICES = [
        ('Roboto', 'Roboto (Padrão)'),
        ('Playfair Display', 'Playfair Display (Elegante)'),
        ('Merriweather', 'Merriweather (Clássico)'),
        ('Montserrat', 'Montserrat (Moderno)'),
        ('Lora', 'Lora (Serifa)'),
        ('Open Sans', 'Open Sans (Clean)'),
        ('PT Serif', 'PT Serif (Jornal)'),
        ('Georgia', 'Georgia (Tradicional)'),
    ]
    
    title_font = models.CharField(
        max_length=100,
        choices=FONT_CHOICES,
        default='Roboto',
        verbose_name="Fonte do Título",
        help_text="Escolha a fonte para o título deste artigo"
    )
    
    introduction = RichTextField(
        max_length=500, 
        verbose_name="Introdução",
        features=['bold', 'italic', 'link'],
        help_text="Introdução do artigo (até 500 caracteres) com formatação básica"
    )
    
    is_premium = models.BooleanField(default=False, verbose_name="Conteúdo Exclusivo?")
    
    # Featured article flag - for high-impact articles
    is_featured_highlight = models.BooleanField(
        default=False,
        verbose_name="Artigo de Alto Impacto?",
        help_text="Marque para destacar este artigo independente da data de publicação"
    )
    
    # Section field
    section = models.CharField(
        max_length=50,
        choices=SECTION_CHOICES,
        default='em-alta',
        verbose_name="Seção",
        help_text="Escolha a seção deste artigo"
    )
    
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

    # Campo legado com recursos completos de edição
    body = RichTextField(
        blank=True, 
        verbose_name="Corpo do Artigo (Legado)",
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'superscript', 'subscript', 'blockquote']
    )
    
    # Novo campo StreamField para conteúdo moderno e flexível
    content_blocks = StreamField([
        ('paragraph', blocks.RichTextBlock(
            label="Parágrafo",
            features=['h2', 'h3', 'h4', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'code', 'superscript', 'subscript', 'blockquote'],
            help_text="Adicione parágrafos de texto com formatação completa"
        )),
        ('heading', blocks.CharBlock(
            label="Título/Subtítulo",
            form_classname="title",
            help_text="Adicione um título de seção"
        )),
        ('image', ImageChooserBlock(
            label="Imagem (Somente Upload)",
            help_text="Insira uma imagem do banco de dados"
        )),
        ('image_url', ImageBlock()),
        ('gif', GifBlock()),
        ('audio', AudioBlock()),
        ('pdf_download', PDFDownloadBlock()),
        ('video', EmbedBlock(
            label="Vídeo (YouTube, Vimeo, etc.)",
            help_text="Cole o link do vídeo do YouTube, Vimeo ou outra plataforma"
        )),
        ('quote', blocks.StructBlock([
            ('text', blocks.TextBlock(label="Texto da Citação")),
            ('author', blocks.CharBlock(required=False, label="Autor")),
        ], label="Citação", icon="openquote")),
        ('list', blocks.ListBlock(
            blocks.CharBlock(label="Item"),
            label="Lista",
            help_text="Adicione uma lista de itens"
        )),
        ('divider', blocks.StaticBlock(
            label="Divisor",
            admin_text="Uma linha horizontal para separar seções",
            template="content/blocks/divider.html"
        )),
        ('html', blocks.RawHTMLBlock(
            label="HTML Customizado",
            help_text="Adicione HTML personalizado (use com cuidado)"
        )),
    ], blank=True, null=True, use_json_field=True, verbose_name="Conteúdo do Artigo")
    
    # Tags para categorização
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    
    # Define what pages can be parents of ArticlePage
    parent_page_types = ['content.HomePage', 'content.SectionPage']

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('publication_date'),
            FieldPanel('section'),
            FieldPanel('is_premium'),
            FieldPanel('is_featured_highlight'),
        ], heading="Configurações do Artigo"),
        MultiFieldPanel([
            FieldPanel('title_font'),
        ], heading="Estilo do Título"),
        MultiFieldPanel([
            FieldPanel('introduction'),
        ], heading="Introdução do Artigo"),
        MultiFieldPanel([
            FieldPanel('featured_image'),
            FieldPanel('external_image_url'),
        ], heading="Imagem de Destaque (escolha uma opção)"),
        FieldPanel('content_blocks'),
        FieldPanel('body'),  # Campo legado com recursos completos
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


class SectionPage(Page):
    """Página de seção para listar artigos de uma categoria específica"""
    section_key = models.CharField(
        max_length=50,
        choices=ArticlePage.SECTION_CHOICES,
        unique=True,
        verbose_name="Seção",
        help_text="Chave da seção que esta página representa"
    )
    
    introduction = models.TextField(
        blank=True,
        verbose_name="Introdução da Seção",
        help_text="Texto introdutório para esta seção"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('section_key'),
        FieldPanel('introduction'),
    ]
    
    # Define parent and child page types
    parent_page_types = ['content.HomePage']
    subpage_types = ['content.ArticlePage']
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all articles in this section
        all_articles = ArticlePage.objects.filter(
            section=self.section_key
        ).live()
        
        # Prioriza artigos marcados como "Alto Impacto" para o destaque
        featured_highlight = all_articles.filter(is_featured_highlight=True).order_by('-publication_date').first()
        
        if featured_highlight:
            # Se existe um artigo de alto impacto, ele é o destaque
            context['featured_article'] = featured_highlight
            # Exclui o artigo de destaque da lista de artigos
            context['articles'] = all_articles.exclude(id=featured_highlight.id).order_by('-publication_date')
        else:
            # Caso contrário, o artigo mais recente é o destaque
            all_articles_ordered = all_articles.order_by('-publication_date')
            context['featured_article'] = all_articles_ordered.first()
            context['articles'] = all_articles_ordered[1:]
        
        context['section_name'] = dict(ArticlePage.SECTION_CHOICES).get(self.section_key)
        
        # Fetch site customizations
        try:
            context['site_customization'] = SiteCustomization.objects.first()
        except:
            context['site_customization'] = None
        
        return context
    
    class Meta:
        verbose_name = "Página de Seção"
        verbose_name_plural = "Páginas de Seção"


class VideosPage(Page):
    """Página dedicada para exibir vídeos curtos (shorts)"""
    introduction = RichTextField(
        blank=True,
        verbose_name="Introdução",
        help_text="Texto introdutório para a página de vídeos"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
    ]
    
    # Define parent page types
    parent_page_types = ['content.HomePage']
    subpage_types = []
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all video shorts ordered by priority and date
        context['videos'] = VideoShort.objects.all()
        
        return context
    
    class Meta:
        verbose_name = "Página de Vídeos"
        verbose_name_plural = "Páginas de Vídeos"


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
