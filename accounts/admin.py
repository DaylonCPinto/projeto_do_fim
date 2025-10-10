# Em accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile

# Inline para mostrar o perfil do usuário na tela de edição do User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil do Assinante'
    fields = ('cpf', 'is_subscriber', 'subscription_date')
    readonly_fields = ('subscription_date',)

# Personalizando o admin do User para incluir o UserProfile inline
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    
    # Adiciona coluna de status de assinatura na lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'subscriber_status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__is_subscriber')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def subscriber_status(self, obj):
        """Exibe o status de assinatura com ícone colorido"""
        try:
            if obj.userprofile.is_subscriber:
                return format_html(
                    '<span style="color: #28a745; font-weight: bold;">✓ Assinante Premium</span>'
                )
            else:
                return format_html(
                    '<span style="color: #6c757d;">✗ Gratuito</span>'
                )
        except UserProfile.DoesNotExist:
            return format_html(
                '<span style="color: #dc3545;">Sem perfil</span>'
            )
    
    subscriber_status.short_description = 'Status da Assinatura'
    
    # Ações em massa para gerenciar assinantes
    actions = ['activate_subscription', 'deactivate_subscription']
    
    def activate_subscription(self, request, queryset):
        """Ativa assinatura para usuários selecionados"""
        count = 0
        for user in queryset:
            try:
                user.userprofile.is_subscriber = True
                user.userprofile.save()
                count += 1
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user, is_subscriber=True)
                count += 1
        
        self.message_user(request, f'{count} usuário(s) teve(ram) a assinatura ativada.')
    
    activate_subscription.short_description = '✓ Ativar assinatura premium'
    
    def deactivate_subscription(self, request, queryset):
        """Desativa assinatura para usuários selecionados"""
        count = 0
        for user in queryset:
            try:
                user.userprofile.is_subscriber = False
                user.userprofile.save()
                count += 1
            except UserProfile.DoesNotExist:
                pass
        
        self.message_user(request, f'{count} usuário(s) teve(ram) a assinatura desativada.')
    
    deactivate_subscription.short_description = '✗ Desativar assinatura premium'

# Admin personalizado para UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'cpf', 'subscriber_status_badge', 'get_date_joined')
    list_filter = ('is_subscriber',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'cpf')
    readonly_fields = ('user', 'get_date_joined', 'get_last_login')
    
    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'cpf', 'get_date_joined', 'get_last_login')
        }),
        ('Status de Assinatura', {
            'fields': ('is_subscriber',),
            'description': 'Ative ou desative o acesso premium deste usuário.'
        }),
    )
    
    def get_email(self, obj):
        """Retorna o email do usuário"""
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def subscriber_status_badge(self, obj):
        """Exibe badge visual do status de assinatura"""
        if obj.is_subscriber:
            return format_html(
                '<span style="background-color: #E3120B; color: white; padding: 5px 12px; '
                'border-radius: 15px; font-size: 11px; font-weight: bold; '
                'text-transform: uppercase;">★ PREMIUM</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 5px 12px; '
                'border-radius: 15px; font-size: 11px; font-weight: bold; '
                'text-transform: uppercase;">☆ GRATUITO</span>'
            )
    subscriber_status_badge.short_description = 'Status'
    
    def get_date_joined(self, obj):
        """Retorna a data de registro do usuário"""
        return obj.user.date_joined.strftime('%d/%m/%Y %H:%M')
    get_date_joined.short_description = 'Data de Registro'
    
    def get_last_login(self, obj):
        """Retorna o último login do usuário"""
        if obj.user.last_login:
            return obj.user.last_login.strftime('%d/%m/%Y %H:%M')
        return 'Nunca'
    get_last_login.short_description = 'Último Login'
    
    # Ações em massa
    actions = ['activate_subscription', 'deactivate_subscription']
    
    def activate_subscription(self, request, queryset):
        """Ativa assinatura para perfis selecionados"""
        count = queryset.update(is_subscriber=True)
        self.message_user(request, f'{count} assinatura(s) ativada(s) com sucesso.')
    activate_subscription.short_description = '✓ Ativar assinatura premium'
    
    def deactivate_subscription(self, request, queryset):
        """Desativa assinatura para perfis selecionados"""
        count = queryset.update(is_subscriber=False)
        self.message_user(request, f'{count} assinatura(s) desativada(s) com sucesso.')
    deactivate_subscription.short_description = '✗ Desativar assinatura premium'

# Re-registrar o UserAdmin com nossas customizações
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customizar títulos do admin
admin.site.site_header = 'Portal de Análise - Administração'
admin.site.site_title = 'Admin Portal'
admin.site.index_title = 'Painel de Controle'
