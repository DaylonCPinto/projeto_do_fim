from django.contrib import admin
from django.utils.html import format_html
from .models import VideoShort, SiteCustomization

@admin.register(VideoShort)
class VideoShortAdmin(admin.ModelAdmin):
    """Admin modernizado para vídeos curtos"""
    list_display = ('title', 'video_preview', 'duration', 'is_featured_badge', 'order', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('order',)
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Informações do Vídeo', {
            'fields': ('title', 'description', 'video_url', 'duration')
        }),
        ('Thumbnail', {
            'fields': ('thumbnail_image', 'thumbnail_url'),
            'description': 'Escolha uma imagem local ou forneça uma URL externa'
        }),
        ('Configurações de Exibição', {
            'fields': ('is_featured', 'order'),
            'description': 'Configure como o vídeo será exibido no site'
        }),
    )
    
    def video_preview(self, obj):
        """Mostra preview do thumbnail do vídeo"""
        thumbnail_url = obj.get_thumbnail_url()
        return format_html(
            '<img src="{}" style="width: 60px; height: auto; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
            thumbnail_url
        )
    video_preview.short_description = 'Preview'
    
    def is_featured_badge(self, obj):
        """Badge visual para status de destaque"""
        if obj.is_featured:
            return format_html(
                '<span style="background-color: #E3120B; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold; '
                'text-transform: uppercase;">★ DESTAQUE</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 4px 12px; '
                'border-radius: 12px; font-size: 11px; font-weight: bold; '
                'text-transform: uppercase;">NORMAL</span>'
            )
    is_featured_badge.short_description = 'Status'
    
    actions = ['mark_as_featured', 'unmark_as_featured']
    
    def mark_as_featured(self, request, queryset):
        """Marca vídeos como destaque"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} vídeo(s) marcado(s) como destaque.')
    mark_as_featured.short_description = '★ Marcar como destaque'
    
    def unmark_as_featured(self, request, queryset):
        """Remove destaque dos vídeos"""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} vídeo(s) removido(s) do destaque.')
    unmark_as_featured.short_description = '☆ Remover destaque'


@admin.register(SiteCustomization)
class SiteCustomizationAdmin(admin.ModelAdmin):
    """Admin para customização do site"""
    
    fieldsets = (
        ('Tipografia', {
            'fields': ('heading_font', 'body_font'),
            'description': 'Configure as fontes do Google Fonts usadas no site'
        }),
        ('Paleta de Cores', {
            'fields': ('primary_color', 'secondary_color'),
            'description': 'Defina as cores principais do site (formato hexadecimal)'
        }),
        ('Layout e Exibição', {
            'fields': ('show_video_section', 'articles_per_page'),
            'description': 'Configure o layout e comportamento da página inicial'
        }),
    )
    
    def has_add_permission(self, request):
        """Permite apenas uma instância de customização"""
        if SiteCustomization.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        """Não permite deletar as configurações"""
        return False

# Customizar a página inicial do admin
admin.site.site_header = 'Portal de Análise - Painel de Administração'
admin.site.site_title = 'Admin Portal'
admin.site.index_title = 'Gerenciamento de Conteúdo'
