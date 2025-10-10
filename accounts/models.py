# Em accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extensão do modelo User para adicionar informações adicionais.
    Criado automaticamente quando um novo usuário se registra.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile'
    )
    is_subscriber = models.BooleanField(
        default=False,
        verbose_name="Assinante Ativo?"
    )
    subscription_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Assinatura"
    )
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"

    def __str__(self):
        return f"Perfil de {self.user.username}"


# Signals para criação automática do UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Cria um UserProfile automaticamente quando um User é criado.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Salva o UserProfile quando o User é salvo.
    Protege contra erros se o profile não existir.
    """
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)