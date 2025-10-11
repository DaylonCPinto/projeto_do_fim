# content/wagtail_hooks.py

from django.utils.html import format_html
from django.templatetags.static import static
from wagtail import hooks
from wagtail.admin.menu import MenuItem

@hooks.register("insert_global_admin_css")
def global_admin_css():
    """Adiciona CSS customizado ao admin do Wagtail"""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/admin/wagtail_custom.css")
    )

@hooks.register("insert_global_admin_js")
def global_admin_js():
    """Adiciona JavaScript customizado ao admin do Wagtail"""
    return format_html(
        """
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Adiciona mensagem de boas-vindas personalizada
            console.log('%c Portal de Análise - Admin Modernizado', 'font-size: 16px; color: #E3120B; font-weight: bold;');
            
            // Melhora a experiência do usuário com tooltips
            const panels = document.querySelectorAll('.panel');
            panels.forEach(panel => {{
                panel.addEventListener('mouseenter', function() {{
                    this.style.transition = 'all 0.3s ease';
                }});
            }});
        }});
        </script>
        """
    )

@hooks.register('construct_main_menu')
def customize_main_menu(request, menu_items):
    """Customiza o menu principal do Wagtail"""
    # Você pode adicionar itens customizados ao menu aqui
    # Por exemplo:
    # menu_items.append(
    #     MenuItem('Vídeos', '/admin/snippets/content/videoshort/', icon_name='media')
    # )
    pass

@hooks.register('before_serve_page')
def set_custom_cache_control(page, request, serve_args, serve_kwargs):
    """Define controle de cache customizado para páginas"""
    # Isso pode ser usado para otimizar o desempenho
    pass
