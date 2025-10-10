# Em accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Inline para mostrar UserProfile junto com User no admin.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'
    fields = ('is_subscriber', 'subscription_date')


class UserAdmin(BaseUserAdmin):
    """
    Customização do admin de User para incluir UserProfile.
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_is_subscriber')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__is_subscriber')
    
    def get_is_subscriber(self, obj):
        return obj.userprofile.is_subscriber if hasattr(obj, 'userprofile') else False
    get_is_subscriber.short_description = 'Assinante'
    get_is_subscriber.boolean = True


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Registrar UserProfile separadamente também
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_subscriber', 'subscription_date')
    list_filter = ('is_subscriber', 'subscription_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('subscription_date',)