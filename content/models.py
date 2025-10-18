"""
Models do aplicativo de conteúdo.

Este módulo contém os modelos principais do CMS, incluindo:
- Blocos de conteúdo customizados (imagem, GIF, áudio, PDF)
- Modelos de página (HomePage, ArticlePage, SectionPage, etc.)
- Snippets (VideoShort, SiteCustomization)
- Configurações de personalização do site

Security Notes:
- Todas as URLs externas são validadas pelo URLField do Django
- RichTextField e StreamField utilizam sanitização automática do Wagtail
- Apenas usuários com permissões de admin podem adicionar HTML customizado
"""

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


class ImageBlock(blocks.StructBlock):
    """
    Bloco de imagem com suporte para upload ou URL externa.
    
    Permite ao editor escolher entre fazer upload de uma imagem
    ou fornecer uma URL externa, oferecendo flexibilidade no
    gerenciamento de imagens.
    """
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
    caption_position = blocks.ChoiceBlock(
        choices=[
            ('text-start', 'Início (Esquerda)'),
            ('text-center', 'Centro'),
            ('text-end', 'Fim (Direita)'),
        ],
        default='text-start',
        required=False,
        label="Posição da Legenda",
        help_text="Escolha onde a legenda e créditos devem aparecer"
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
    credit = blocks.CharBlock(
        required=False,
        label="Crédito"
    )
    caption_position = blocks.ChoiceBlock(
        choices=[
            ('text-start', 'Início (Esquerda)'),
            ('text-center', 'Centro'),
            ('text-end', 'Fim (Direita)'),
        ],
        default='text-start',
        required=False,
        label="Posição da Legenda",
        help_text="Escolha onde a legenda e créditos devem aparecer"
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


# Custom block for externally hosted videos
class CustomVideoBlock(blocks.StructBlock):
    """Block that renders a customizable HTML5 video player."""

    WIDTH_CHOICES = [
        ("narrow", "Estreito (até 640px)"),
        ("standard", "Padrão (até 860px)"),
        ("wide", "Amplo (até 1040px)"),
        ("full", "Largura Total"),
    ]

    ASPECT_RATIO_CHOICES = [
        ("16x9", "16:9 (Widescreen)"),
        ("4x3", "4:3 (Clássico)"),
        ("1x1", "1:1 (Quadrado)"),
        ("21x9", "21:9 (Cinemascope)"),
    ]

    MIME_TYPE_CHOICES = [
        ("video/mp4", "MP4 (video/mp4)"),
        ("video/webm", "WebM (video/webm)"),
        ("video/ogg", "Ogg/Theora (video/ogg)"),
    ]

    video_url = blocks.URLBlock(
        label="URL do Vídeo",
        help_text="Cole o link direto do arquivo hospedado (MP4, WebM, etc.)",
    )
    mime_type = blocks.ChoiceBlock(
        choices=MIME_TYPE_CHOICES,
        default="video/mp4",
        label="Formato do Vídeo",
        help_text="Selecione o formato/mime type correspondente ao arquivo",
    )
    poster_image = ImageChooserBlock(
        required=False,
        label="Thumbnail do Vídeo (Upload)",
        help_text="Imagem exibida antes da reprodução (opcional)",
    )
    poster_image_url = blocks.URLBlock(
        required=False,
        label="Thumbnail do Vídeo (URL externa)",
        help_text="Opcionalmente use uma imagem hospedada externamente",
    )
    caption = blocks.CharBlock(
        required=False,
        label="Legenda",
        help_text="Texto curto exibido abaixo do player (opcional)",
    )
    width = blocks.ChoiceBlock(
        choices=WIDTH_CHOICES,
        default="standard",
        label="Largura do Player",
        help_text="Controle a largura máxima do player dentro do artigo",
    )
    aspect_ratio = blocks.ChoiceBlock(
        choices=ASPECT_RATIO_CHOICES,
        default="16x9",
        label="Proporção do Vídeo",
        help_text="Escolha a proporção para manter o vídeo responsivo",
    )

    def clean(self, value):
        """Ensure that only one poster source is used when both are provided."""
        cleaned = super().clean(value)
        poster_upload = cleaned.get("poster_image")
        poster_url = cleaned.get("poster_image_url")
        if poster_upload and poster_url:
            raise ValidationError({
                "poster_image_url": "Utilize apenas uma fonte para o thumbnail do vídeo (upload OU URL externa).",
            })
        return cleaned

    class Meta:
        icon = "media"
        label = "Vídeo Personalizado (CDN)"
        template = "content/blocks/custom_video_block.html"


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


# Custom block for Source Link (Fonte com Link)
class FonteLinkBlock(blocks.StructBlock):
    """Block for displaying a source link with custom styled text"""
    texto = blocks.CharBlock(
        required=True,
        label="Texto da Fonte",
        help_text="Texto que aparecerá clicável (ex: CNN, Reuters, BBC)"
    )
    link = blocks.URLBlock(
        required=True,
        label="URL da Fonte",
        help_text="Link completo para a fonte (ex: https://www.cnnbrasil.com.br/...)"
    )
    
    class Meta:
        icon = "link"
        label = "Fonte com Link"
        template = "content/blocks/fonte_link_block.html"


class HomeCuratedSectionBlock(blocks.StructBlock):
    """Bloco que permite montar seções editáveis na home via painel."""

    LAYOUT_CHOICES = [
        ("grid", "Grade Equilibrada"),
        ("list", "Lista Editorial"),
        ("split", "Destaque + Lista")
    ]

    ACCENT_CHOICES = [
        ("economist-red", "Vermelho The Economist"),
        ("ink", "Azul Escuro"),
        ("charcoal", "Cinza Carvão"),
        ("sand", "Areia Quente"),
    ]

    title = blocks.CharBlock(label="Título da Seção")
    subtitle = blocks.TextBlock(required=False, label="Linha de Apoio")
    layout_style = blocks.ChoiceBlock(
        choices=LAYOUT_CHOICES,
        default="grid",
        label="Estilo da Listagem"
    )
    accent = blocks.ChoiceBlock(
        choices=ACCENT_CHOICES,
        default="economist-red",
        label="Cor de Destaque"
    )
    call_to_action_text = blocks.CharBlock(
        required=False,
        label="Texto do Link/CTA"
    )
    call_to_action_url = blocks.URLBlock(
        required=False,
        label="URL do CTA",
        help_text="Opcional – deixa a seção com um link "
                  "para ver todos os artigos da editoria"
    )
    articles = blocks.ListBlock(
        blocks.PageChooserBlock(target_model="content.ArticlePage"),
        min_num=1,
        label="Artigos Selecionados",
        help_text="Escolha manualmente quais artigos aparecem nesta seção"
    )

    class Meta:
        icon = "pick"
        label = "Seção Curada (Home)"
        template = "content/blocks/home_curated_section.html"


class HomePage(Page):
    """Página inicial do site com configurações customizáveis"""
    
    body = RichTextField(blank=True, verbose_name="Corpo da Página")
    
    # Footer tagline customization
    footer_tagline = models.CharField(
        max_length=200,
        default="Reconstruindo o sentido no fim da era antiga.",
        verbose_name="Frase do Rodapé",
        help_text="Texto que aparece no rodapé do site"
    )
    
    TAGLINE_SIZE_CHOICES = [
        ('0.6rem', 'Muito Pequeno'),
        ('0.7rem', 'Pequeno (Padrão)'),
        ('0.8rem', 'Médio'),
        ('0.9rem', 'Grande'),
        ('1rem', 'Muito Grande'),
        ('1.1rem', 'Extra Grande'),
    ]
    
    footer_tagline_size = models.CharField(
        max_length=20,
        choices=TAGLINE_SIZE_CHOICES,
        default='0.7rem',
        verbose_name="Tamanho da Frase do Rodapé",
        help_text="Escolha o tamanho da frase que aparece no rodapé"
    )
    
    # Layout configuration for homepage
    LAYOUT_PRESET_CHOICES = [
        ('three_column_grid', 'Grade de 3 Colunas (Padrão)'),
        ('two_column_grid', 'Grade de 2 Colunas'),
        ('list_with_dividers', 'Lista com Divisores'),
        ('feature_top_grid', 'Destaque no Topo + Grade'),
        ('masonry_light', 'Masonry Leve (Pinterest-style)'),
    ]
    
    home_layout_preset = models.CharField(
        max_length=50,
        choices=LAYOUT_PRESET_CHOICES,
        default='three_column_grid',
        verbose_name="Preset de Layout da Home",
        help_text="Escolha o estilo de layout para a página inicial"
    )
    
    COLUMN_CHOICES = [
        (1, '1 Coluna'),
        (2, '2 Colunas'),
        (3, '3 Colunas'),
        (4, '4 Colunas'),
    ]
    
    columns_desktop = models.IntegerField(
        choices=COLUMN_CHOICES,
        default=3,
        verbose_name="Colunas (Desktop)",
        help_text="Número de colunas no desktop (>= 1024px)"
    )
    
    columns_mobile = models.IntegerField(
        choices=[(1, '1 Coluna'), (2, '2 Colunas')],
        default=1,
        verbose_name="Colunas (Mobile)",
        help_text="Número de colunas no mobile (< 768px)"
    )
    
    GAP_CHOICES = [
        ('0.5rem', 'Pequeno (0.5rem)'),
        ('1rem', 'Médio (1rem)'),
        ('1.5rem', 'Grande (1.5rem)'),
        ('2rem', 'Extra Grande (2rem)'),
    ]
    
    grid_gap = models.CharField(
        max_length=20,
        choices=GAP_CHOICES,
        default='1rem',
        verbose_name="Espaçamento entre Cards",
        help_text="Espaço entre os cards de artigos"
    )

    show_dividers = models.BooleanField(
        default=False,
        verbose_name="Mostrar Divisores?",
        help_text="Adiciona linhas divisórias entre artigos (melhor para layout de lista)"
    )

    DIVIDER_STYLE_CHOICES = [
        ('thin', 'Linha Fina Clássica'),
        ('thick', 'Linha Grossa Editorial'),
        ('double', 'Linha Dupla'),
    ]

    divider_style = models.CharField(
        max_length=20,
        choices=DIVIDER_STYLE_CHOICES,
        default='thin',
        verbose_name="Estilo dos Divisores",
        help_text="Define como as linhas divisórias aparecem entre as seções"
    )

    hero_kicker = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Kicker do Destaque",
        help_text="Linha superior curta, ex: 'Análise Especial'"
    )

    hero_subtitle = models.TextField(
        blank=True,
        verbose_name="Resumo Editorial",
        help_text="Texto que aparece ao lado do artigo em destaque"
    )

    hero_button_text = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Texto do Botão",
        help_text="Etiqueta do botão exibido no destaque principal"
    )

    hero_button_url = models.URLField(
        blank=True,
        verbose_name="URL do Botão",
        help_text="Link opcional para guiar o leitor (ex: assinatura, newsletter)"
    )

    hero_background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagem de Fundo do Destaque",
        help_text="Imagem aplicada como textura sutil atrás do destaque"
    )

    VIDEO_SECTION_POSITION_CHOICES = [
        ('below_highlight', 'Abaixo do destaque principal'),
        ('below_recent', 'Abaixo de "Análises Recentes"'),
    ]

    show_videos_section = models.BooleanField(
        default=True,
        verbose_name="Mostrar seção de vídeos?"
    )

    video_section_position = models.CharField(
        max_length=30,
        choices=VIDEO_SECTION_POSITION_CHOICES,
        default='below_highlight',
        verbose_name="Posição dos vídeos curtos",
        help_text="Controle se a vitrine de vídeos fica abaixo do destaque principal ou das análises recentes."
    )

    curated_sections = StreamField(
        [
            ("curated_section", HomeCuratedSectionBlock())
        ],
        blank=True,
        use_json_field=True,
        verbose_name="Seções Editoriais Curadas"
    )

    show_trending_section = models.BooleanField(
        default=True,
        verbose_name="Mostrar Seção 'Em Alta'?",
        help_text="Exibe ou oculta a seção de artigos em alta"
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('home_layout_preset'),
            FieldPanel('columns_desktop'),
            FieldPanel('columns_mobile'),
            FieldPanel('grid_gap'),
            FieldPanel('show_dividers'),
            FieldPanel('divider_style'),
            FieldPanel('show_trending_section'),
            FieldPanel('show_videos_section'),
            FieldPanel('video_section_position'),
        ], heading="Configurações de Layout da Home"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('hero_kicker'),
                FieldPanel('hero_button_text'),
            ]),
            FieldPanel('hero_subtitle'),
            FieldRowPanel([
                FieldPanel('hero_button_url'),
                FieldPanel('hero_background_image'),
            ]),
        ], heading="Destaque Principal"),
        MultiFieldPanel([
            FieldPanel('footer_tagline'),
            FieldPanel('footer_tagline_size'),
        ], heading="Configurações do Rodapé"),
        FieldPanel('curated_sections'),
    ]
    
    # Define what types of pages can be children of HomePage
    subpage_types = ['content.SectionPage', 'content.ArticlePage', 'content.VideosPage', 'content.SupportSectionPage']
    
    def get_layout_config(self):
        """
        Returns a dictionary with layout configuration.
        Used in templates to apply dynamic styling.
        """
        return {
            'preset': self.home_layout_preset,
            'columns_desktop': self.columns_desktop,
            'columns_mobile': self.columns_mobile,
            'grid_gap': self.grid_gap,
            'show_dividers': self.show_dividers,
            'show_trending_section': self.show_trending_section,
            'divider_style': self.divider_style,
            # CSS class helpers
            'grid_cols_desktop': f'lg:grid-cols-{self.columns_desktop}',
            'grid_cols_mobile': f'grid-cols-{self.columns_mobile}',
            'layout_class': f'layout-{self.home_layout_preset}',
        }
    
    def clean(self):
        """
        Validação customizada do modelo.
        
        Garante que a tagline do rodapé não esteja vazia e tenha
        um tamanho razoável para exibição.
        
        Raises:
            ValidationError: Se a validação falhar
        """
        super().clean()
        
        if self.footer_tagline and len(self.footer_tagline.strip()) < 10:
            raise ValidationError({
                'footer_tagline': 'A frase do rodapé deve ter pelo menos 10 caracteres.'
            })

    def get_context(self, request, *args, **kwargs):
        """
        Adiciona dados customizados ao contexto da página inicial.
        
        Returns:
            dict: Contexto com artigos, vídeos e configurações do site
        """
        context = super().get_context(request, *args, **kwargs)

        # Busca todos os artigos descendentes
        all_articles = ArticlePage.objects.descendant_of(self).live()
        
        # 1. DESTAQUE PRINCIPAL (fixo manualmente)
        featured_highlight = all_articles.filter(is_featured_highlight=True).order_by('-publication_date').first()
        context['featured_article'] = featured_highlight
        
        # Exclude featured article from other listings
        remaining_articles = all_articles.exclude(id=featured_highlight.id) if featured_highlight else all_articles
        
        # 2. NOTÍCIAS "EM ALTA" (automáticas ou manuais)
        # Filter articles that are currently trending
        trending_articles = []
        for article in remaining_articles:
            if article.is_currently_trending():
                trending_articles.append(article)
        
        # Sort trending by publication date (most recent first)
        trending_articles = sorted(trending_articles, key=lambda x: x.publication_date, reverse=True)
        context['trending_articles'] = trending_articles
        
        # Get IDs of articles already shown
        shown_ids = [featured_highlight.id] if featured_highlight else []
        shown_ids.extend([a.id for a in trending_articles])
        
        # 3. ARTIGOS REGULARES E PREMIUM (todos visíveis nas listagens)
        regular_articles = remaining_articles.exclude(id__in=shown_ids)
        
        # Check if user is authenticated and is a premium subscriber
        user = request.user
        is_premium_subscriber = (
            user.is_authenticated and 
            hasattr(user, 'userprofile') and
            user.userprofile.is_subscriber
        )
        
        # TODOS os artigos aparecem nas listagens (incluindo premium)
        # O controle de acesso ao conteúdo completo é feito no template do artigo
        
        context['articles'] = regular_articles.order_by('-publication_date')
        context['is_premium_subscriber'] = is_premium_subscriber
        
        # Busca vídeos curtos destacados respeitando prioridade
        featured_videos_qs = VideoShort.objects.filter(is_featured=True).order_by('order', '-created_at')
        context['featured_videos'] = featured_videos_qs[:6]
        
        # Busca customizações do site
        try:
            site_customization = SiteCustomization.objects.first()
        except SiteCustomization.DoesNotExist:
            site_customization = None

        context['site_customization'] = site_customization
        context['show_video_shorts'] = (
            bool(context['featured_videos'])
            and self.show_videos_section
            and (site_customization.show_video_section if site_customization else True)
        )
        
        # Adiciona a home_page ao contexto para uso no footer
        context['home_page'] = self
        
        # Add layout configuration to context
        context['layout_config'] = self.get_layout_config()

        return context


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
    
    # Trending article flag
    is_trending = models.BooleanField(
        default=False,
        verbose_name="Em Alta?",
        help_text="Artigos marcados como 'Em Alta' aparecem com destaque e emoji de fogo. Novos artigos são automaticamente marcados por 3 horas."
    )
    
    trending_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Em Alta Até",
        help_text="Data/hora até quando o artigo permanecerá em alta (automático para novos artigos)"
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
    
    highlight_video_url = models.URLField(
        blank=True,
        verbose_name="URL do Vídeo de Destaque",
        help_text="Link direto para um vídeo hospedado externamente (MP4, WebM, etc.) para uso no destaque da home.",
    )

    HIGHLIGHT_VIDEO_MIME_CHOICES = [
        ('video/mp4', 'MP4 (video/mp4)'),
        ('video/webm', 'WebM (video/webm)'),
        ('video/ogg', 'Ogg/Theora (video/ogg)'),
    ]

    highlight_video_mime_type = models.CharField(
        max_length=20,
        choices=HIGHLIGHT_VIDEO_MIME_CHOICES,
        default='video/mp4',
        verbose_name="Formato do Vídeo de Destaque",
        help_text="Seleciona o mime type usado ao renderizar o vídeo de destaque.",
    )

    highlight_video_poster = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Thumbnail do Vídeo de Destaque",
    )

    highlight_video_poster_url = models.URLField(
        blank=True,
        verbose_name="Thumbnail Externo do Vídeo de Destaque",
        help_text="URL opcional para imagem de capa do vídeo quando hospedada externamente.",
    )

    # Caption and credits for featured image
    featured_image_caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Legenda da Imagem de Destaque",
        help_text="Legenda descritiva para a imagem de destaque"
    )
    
    featured_image_credit = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Créditos da Imagem de Destaque",
        help_text="Créditos/fonte da imagem (ex: Foto de João Silva/Reuters)"
    )
    
    # Caption position choices
    CAPTION_POSITION_CHOICES = [
        ('text-start', 'Início (Esquerda)'),
        ('text-center', 'Centro'),
        ('text-end', 'Fim (Direita)'),
    ]
    
    featured_image_caption_position = models.CharField(
        max_length=20,
        choices=CAPTION_POSITION_CHOICES,
        default='text-start',
        verbose_name="Posição da Legenda",
        help_text="Escolha onde a legenda e créditos devem aparecer"
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
        ('custom_video', CustomVideoBlock()),
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
        ('fonte_link', FonteLinkBlock()),
        ('html', blocks.RawHTMLBlock(
            label="HTML Customizado",
            help_text="Adicione HTML personalizado (use com cuidado)"
        )),
    ], blank=True, null=True, use_json_field=True, verbose_name="Conteúdo do Artigo")
    
    # Tags para categorização
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    
    # Define what pages can be parents of ArticlePage
    parent_page_types = ['content.HomePage', 'content.SectionPage', 'content.SupportSectionPage']

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('publication_date'),
            FieldPanel('section'),
            FieldPanel('is_premium'),
            FieldPanel('is_featured_highlight'),
            FieldPanel('is_trending'),
            FieldPanel('trending_until'),
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
            FieldPanel('highlight_video_url'),
            FieldPanel('highlight_video_mime_type'),
            FieldPanel('highlight_video_poster'),
            FieldPanel('highlight_video_poster_url'),
            FieldPanel('featured_image_caption'),
            FieldPanel('featured_image_credit'),
            FieldPanel('featured_image_caption_position'),
        ], heading="Mídia de Destaque (imagem ou vídeo)"),
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

    def has_highlight_video(self):
        """Retorna True quando um vídeo customizado de destaque foi configurado."""
        return bool(self.highlight_video_url)

    def get_highlight_video_poster_url(self):
        """Obtém a melhor imagem de poster disponível para o vídeo de destaque."""
        if self.highlight_video_poster:
            try:
                return self.highlight_video_poster.file.url
            except Exception:
                pass
            return self.highlight_video_poster.file.url
        if self.highlight_video_poster_url:
            return self.highlight_video_poster_url
        return None

    def clean(self):
        cleaned = super().clean()
        if self.highlight_video_poster and self.highlight_video_poster_url:
            raise ValidationError({
                'highlight_video_poster_url': "Escolha apenas uma forma de definir o thumbnail do vídeo de destaque (upload OU URL externa).",
            })
        return cleaned
    
    def save(self, *args, **kwargs):
        """Override save to automatically set trending for new articles"""
        from datetime import timedelta
        
        # Check if this is a new article being published
        is_new = self.pk is None
        
        # Call parent save first
        super().save(*args, **kwargs)
        
        # If it's a new article, automatically set it as trending for 3 hours
        if is_new and self.live:
            self.is_trending = True
            self.trending_until = timezone.now() + timedelta(hours=3)
            # Save again to update trending fields
            super().save(update_fields=['is_trending', 'trending_until'])
    
    def is_currently_trending(self):
        """Check if article is currently trending (considers both manual and automatic trending)"""
        if not self.is_trending:
            return False
        
        # If trending_until is set and has passed, return False
        if self.trending_until and timezone.now() > self.trending_until:
            return False
        
        return True
    
    def get_context(self, request, *args, **kwargs):
        """
        Add subscriber status to context for paywall logic.
        
        Returns:
            dict: Context with is_subscriber flag
        """
        context = super().get_context(request, *args, **kwargs)
        
        # Safely check if user is a subscriber
        user = request.user
        context['is_subscriber'] = (
            user.is_authenticated and 
            hasattr(user, 'userprofile') and
            user.userprofile.is_subscriber
        )
        
        return context


@register_snippet
class VideoShort(models.Model):
    """Modelo para vídeos curtos (shorts)"""

    VIDEO_SOURCE_CHOICES = [
        ('platform', 'Plataforma (YouTube, Vimeo, etc.)'),
        ('cdn', 'Arquivo direto em CDN'),
    ]

    VIDEO_MIME_CHOICES = [
        ('video/mp4', 'MP4 (video/mp4)'),
        ('video/webm', 'WebM (video/webm)'),
        ('video/ogg', 'Ogg/Theora (video/ogg)'),
    ]

    title = models.CharField(max_length=100, verbose_name="Título do Vídeo")
    description = models.TextField(max_length=250, blank=True, verbose_name="Descrição")
    
    # Opções de vídeo
    video_url = models.URLField(
        verbose_name="URL do Vídeo",
        help_text="URL do vídeo (YouTube, Vimeo, etc.)",
        blank=True,
    )

    video_source_type = models.CharField(
        max_length=20,
        choices=VIDEO_SOURCE_CHOICES,
        default='platform',
        verbose_name="Origem do Vídeo",
        help_text="Escolha entre incorporar de uma plataforma ou carregar o player com um arquivo em CDN.",
    )

    cdn_video_url = models.URLField(
        blank=True,
        verbose_name="URL do Vídeo (CDN)",
        help_text="Forneça o link direto (MP4, WebM, etc.) quando utilizar um arquivo próprio em CDN.",
    )

    cdn_mime_type = models.CharField(
        max_length=20,
        choices=VIDEO_MIME_CHOICES,
        blank=True,
        verbose_name="Formato do Vídeo (CDN)",
        help_text="Obrigatório para arquivos diretos. Ajuda os navegadores a detectar o formato corretamente.",
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
        FieldPanel('video_source_type'),
        FieldPanel('video_url'),
        FieldPanel('cdn_video_url'),
        FieldPanel('cdn_mime_type'),
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
            try:
                return self.thumbnail_image.file.url
            except Exception:
                return 'https://via.placeholder.com/400x700/E3120B/FFFFFF?text=Video'
        return 'https://via.placeholder.com/400x700/E3120B/FFFFFF?text=Video'

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()

        if self.thumbnail_image and self.thumbnail_url:
            raise ValidationError({
                'thumbnail_url': 'Escolha apenas uma fonte para o thumbnail (upload OU URL externa).'
            })

        if self.video_source_type == 'platform' and not self.video_url:
            raise ValidationError({
                'video_url': 'Informe a URL da plataforma quando o tipo for Plataforma.'
            })

        if self.video_source_type == 'cdn':
            errors = {}
            if not self.cdn_video_url:
                errors['cdn_video_url'] = 'Informe o link direto do arquivo hospedado na CDN.'
            if not self.cdn_mime_type:
                errors['cdn_mime_type'] = 'Selecione o formato correspondente ao arquivo hospedado.'
            if errors:
                raise ValidationError(errors)

    def uses_cdn(self):
        return self.video_source_type == 'cdn' and bool(self.cdn_video_url)

    def get_cdn_source(self):
        return self.cdn_video_url if self.uses_cdn() else ''

    def get_cdn_mime(self):
        return self.cdn_mime_type if self.uses_cdn() else ''

    def get_embed_url(self):
        """Converte links conhecidos em URLs incorporáveis."""
        if self.uses_cdn() or not self.video_url:
            return ''

        url = self.video_url

        if 'youtube.com/watch' in url:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            video_id = parse_qs(parsed.query).get('v', [''])[0]
            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'
        if 'youtu.be/' in url:
            video_id = url.rstrip('/').split('/')[-1]
            if video_id:
                return f'https://www.youtube.com/embed/{video_id}'
        if 'vimeo.com/' in url:
            video_id = url.rstrip('/').split('/')[-1]
            if video_id.isdigit():
                return f'https://player.vimeo.com/video/{video_id}'

        return url


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
    
    # Title customization
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
    
    SIZE_CHOICES = [
        ('1rem', 'Muito Pequeno (1rem)'),
        ('1.5rem', 'Pequeno (1.5rem)'),
        ('2rem', 'Médio (2rem)'),
        ('2.5rem', 'Grande (2.5rem)'),
        ('3rem', 'Muito Grande (3rem)'),
        ('3.5rem', 'Extra Grande (3.5rem)'),
        ('4rem', 'Enorme (4rem)'),
    ]
    
    title_font = models.CharField(
        max_length=100,
        choices=FONT_CHOICES,
        default='Roboto',
        verbose_name="Fonte do Título",
        help_text="Escolha a fonte para o título da seção"
    )
    
    title_size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        default='3rem',
        verbose_name="Tamanho do Título",
        help_text="Escolha o tamanho do título da seção"
    )
    
    subtitle_font = models.CharField(
        max_length=100,
        choices=FONT_CHOICES,
        default='Merriweather',
        verbose_name="Fonte do Subtítulo",
        help_text="Escolha a fonte para o subtítulo/introdução da seção"
    )
    
    subtitle_size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        default='2rem',
        verbose_name="Tamanho do Subtítulo",
        help_text="Escolha o tamanho do subtítulo/introdução da seção"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('section_key'),
        FieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('title_font'),
            FieldPanel('title_size'),
        ], heading="Personalização do Título"),
        MultiFieldPanel([
            FieldPanel('subtitle_font'),
            FieldPanel('subtitle_size'),
        ], heading="Personalização do Subtítulo"),
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
        
        # 1. DESTAQUE PRINCIPAL (fixo manualmente)
        featured_highlight = all_articles.filter(is_featured_highlight=True).order_by('-publication_date').first()
        context['featured_article'] = featured_highlight
        
        # Exclude featured article from other listings
        remaining_articles = all_articles.exclude(id=featured_highlight.id) if featured_highlight else all_articles
        
        # 2. NOTÍCIAS "EM ALTA" (automáticas ou manuais)
        trending_articles = []
        for article in remaining_articles:
            if article.is_currently_trending():
                trending_articles.append(article)
        
        trending_articles = sorted(trending_articles, key=lambda x: x.publication_date, reverse=True)
        context['trending_articles'] = trending_articles
        
        # Get IDs of articles already shown
        shown_ids = [featured_highlight.id] if featured_highlight else []
        shown_ids.extend([a.id for a in trending_articles])
        
        # 3. ARTIGOS REGULARES E PREMIUM (todos visíveis nas listagens)
        regular_articles = remaining_articles.exclude(id__in=shown_ids)
        
        # Check if user is authenticated and is a premium subscriber
        user = request.user
        is_premium_subscriber = (
            user.is_authenticated and 
            hasattr(user, 'userprofile') and
            user.userprofile.is_subscriber
        )
        
        # TODOS os artigos aparecem nas listagens (incluindo premium)
        # O controle de acesso ao conteúdo completo é feito no template do artigo
        
        context['articles'] = regular_articles.order_by('-publication_date')
        context['is_premium_subscriber'] = is_premium_subscriber
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


class SupportSectionPage(Page):
    """Página de seção de apoio para artigos e guias auxiliares"""
    introduction = models.TextField(
        blank=True,
        verbose_name="Introdução da Seção de Apoio",
        help_text="Texto introdutório para esta seção de apoio"
    )
    
    # Title customization
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
    
    SIZE_CHOICES = [
        ('1rem', 'Muito Pequeno (1rem)'),
        ('1.5rem', 'Pequeno (1.5rem)'),
        ('2rem', 'Médio (2rem)'),
        ('2.5rem', 'Grande (2.5rem)'),
        ('3rem', 'Muito Grande (3rem)'),
        ('3.5rem', 'Extra Grande (3.5rem)'),
        ('4rem', 'Enorme (4rem)'),
    ]
    
    title_font = models.CharField(
        max_length=100,
        choices=FONT_CHOICES,
        default='Roboto',
        verbose_name="Fonte do Título",
        help_text="Escolha a fonte para o título da seção"
    )
    
    title_size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        default='3rem',
        verbose_name="Tamanho do Título",
        help_text="Escolha o tamanho do título da seção"
    )
    
    subtitle_font = models.CharField(
        max_length=100,
        choices=FONT_CHOICES,
        default='Merriweather',
        verbose_name="Fonte do Subtítulo",
        help_text="Escolha a fonte para o subtítulo/introdução da seção"
    )
    
    subtitle_size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        default='2rem',
        verbose_name="Tamanho do Subtítulo",
        help_text="Escolha o tamanho do subtítulo/introdução da seção"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel([
            FieldPanel('title_font'),
            FieldPanel('title_size'),
        ], heading="Personalização do Título"),
        MultiFieldPanel([
            FieldPanel('subtitle_font'),
            FieldPanel('subtitle_size'),
        ], heading="Personalização do Subtítulo"),
    ]
    
    # Define parent and child page types
    parent_page_types = ['content.HomePage']
    subpage_types = ['content.ArticlePage']
    
    def get_url_parts(self, request=None):
        """Override to add /subsecao/ prefix to support section URLs"""
        url_parts = super().get_url_parts(request=request)
        
        if url_parts is None:
            return None
            
        site_id, root_url, page_path = url_parts
        
        # Add /subsecao/ prefix before the page slug
        if page_path and not page_path.startswith('/subsecao/'):
            page_path = f'/subsecao{page_path}'
        
        return (site_id, root_url, page_path)
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        # Get all articles in this support section
        all_articles = ArticlePage.objects.descendant_of(self).live()
        
        # 1. DESTAQUE PRINCIPAL (fixo manualmente)
        featured_highlight = all_articles.filter(is_featured_highlight=True).order_by('-publication_date').first()
        context['featured_article'] = featured_highlight
        
        # Exclude featured article from other listings
        remaining_articles = all_articles.exclude(id=featured_highlight.id) if featured_highlight else all_articles
        
        # 2. NOTÍCIAS "EM ALTA" (automáticas ou manuais)
        trending_articles = []
        for article in remaining_articles:
            if article.is_currently_trending():
                trending_articles.append(article)
        
        trending_articles = sorted(trending_articles, key=lambda x: x.publication_date, reverse=True)
        context['trending_articles'] = trending_articles
        
        # Get IDs of articles already shown
        shown_ids = [featured_highlight.id] if featured_highlight else []
        shown_ids.extend([a.id for a in trending_articles])
        
        # 3. ARTIGOS REGULARES E PREMIUM (todos visíveis nas listagens)
        regular_articles = remaining_articles.exclude(id__in=shown_ids)
        
        # Check if user is authenticated and is a premium subscriber
        user = request.user
        is_premium_subscriber = (
            user.is_authenticated and 
            hasattr(user, 'userprofile') and
            user.userprofile.is_subscriber
        )
        
        # TODOS os artigos aparecem nas listagens (incluindo premium)
        # O controle de acesso ao conteúdo completo é feito no template do artigo
        
        context['articles'] = regular_articles.order_by('-publication_date')
        context['is_premium_subscriber'] = is_premium_subscriber
        
        # Fetch site customizations
        try:
            context['site_customization'] = SiteCustomization.objects.first()
        except:
            context['site_customization'] = None
        
        return context
    
    class Meta:
        verbose_name = "Seção de Apoio"
        verbose_name_plural = "Seções de Apoio"


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

    show_scroll_progress = models.BooleanField(
        default=True,
        verbose_name="Exibir barra de progresso de leitura?",
        help_text="Controla a barra fina no topo que indica o quanto do artigo já foi lido."
    )

    enable_dark_mode_toggle = models.BooleanField(
        default=False,
        verbose_name="Mostrar alternância de modo escuro?",
        help_text="Exibe um botão no menu para que os leitores alternem entre modo claro e escuro."
    )

    announcement_enabled = models.BooleanField(
        default=False,
        verbose_name="Ativar barra de anúncio/editorial?",
        help_text="Mostra uma faixa acima do cabeçalho com mensagens editoriais ou campanhas."
    )

    announcement_text = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Mensagem do anúncio",
        help_text="Texto curto exibido na barra promocional do topo."
    )

    announcement_link_text = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Texto do botão do anúncio",
        help_text="Opcional. Se preenchido, um botão será exibido ao lado da mensagem."
    )

    announcement_link_url = models.URLField(
        blank=True,
        verbose_name="Link do anúncio",
        help_text="URL aberta ao clicar no botão da barra promocional."
    )

    whatsapp_contact_url = models.URLField(
        blank=True,
        verbose_name="Link de contato (WhatsApp/Telegram)",
        help_text="Exibe um botão flutuante para contato rápido via WhatsApp, Telegram ou similar."
    )

    short_videos_title = models.CharField(
        max_length=80,
        default="Vídeos em Destaque",
        verbose_name="Título da seção de vídeos",
        help_text="Texto exibido no topo da vitrine de vídeos curtos."
    )

    short_videos_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Descrição da seção de vídeos",
        help_text="Linha auxiliar exibida abaixo do título (opcional)."
    )

    short_videos_cta_label = models.CharField(
        max_length=40,
        default="Ver todos",
        blank=True,
        verbose_name="Texto do link da seção de vídeos",
        help_text="Etiqueta do link de ação ao lado do título. Deixe em branco para ocultar."
    )

    short_videos_cta_url = models.URLField(
        blank=True,
        verbose_name="URL do link da seção de vídeos",
        help_text="Para onde o visitante é levado ao clicar no CTA da seção de vídeos."
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
            FieldPanel('show_scroll_progress'),
            FieldPanel('enable_dark_mode_toggle'),
            FieldPanel('articles_per_page'),
        ], heading="Layout"),
        MultiFieldPanel([
            FieldPanel('announcement_enabled'),
            FieldPanel('announcement_text'),
            FieldPanel('announcement_link_text'),
            FieldPanel('announcement_link_url'),
        ], heading="Barra de anúncio"),
        MultiFieldPanel([
            FieldPanel('short_videos_title'),
            FieldPanel('short_videos_description'),
            FieldPanel('short_videos_cta_label'),
            FieldPanel('short_videos_cta_url'),
        ], heading="Vitrine de vídeos"),
        FieldPanel('whatsapp_contact_url'),
    ]
    
    class Meta:
        verbose_name = "Customização do Site"
        verbose_name_plural = "Customização do Site"

    def __str__(self):
        return "Configurações de Customização do Site"

    def clean(self):
        super().clean()

        from django.core.exceptions import ValidationError

        if self.announcement_enabled and not self.announcement_text:
            raise ValidationError({
                'announcement_text': 'Informe a mensagem que será exibida na barra de anúncio.'
            })

        if self.announcement_link_text and not self.announcement_link_url:
            raise ValidationError({
                'announcement_link_url': 'Forneça o link que será aberto ao clicar no botão da barra.'
            })

        if self.announcement_link_url and not self.announcement_link_text:
            raise ValidationError({
                'announcement_link_text': 'Informe o texto do botão para o link configurado.'
            })

        if self.short_videos_cta_url and not self.short_videos_cta_label:
            raise ValidationError({
                'short_videos_cta_label': 'Informe o texto do link da seção de vídeos ou deixe ambos os campos vazios.'
            })
