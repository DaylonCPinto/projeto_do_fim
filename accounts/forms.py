"""Formulários de autenticação e registro com validação reforçada."""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .validators import (
    validate_cpf, 
    validate_allowed_email_domains, 
    validate_username_format,
    validate_email_characters
)
import re
import bleach


class EmailAuthenticationForm(AuthenticationForm):
    """Permite autenticação usando e-mail em vez do username padrão."""
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label='Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class SignUpForm(UserCreationForm):
    """Formulário de cadastro com validação de e-mail, CPF e usuário."""
    email = forms.EmailField(
        required=True,
        label='E-mail',
        help_text='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'id_email'
        })
    )
    
    cpf = forms.CharField(
        max_length=14,
        required=True,
        label='CPF',
        help_text='000.000.000-00',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00',
            'id': 'id_cpf',
            'maxlength': '14'
        })
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'cpf', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'id_password1'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'id_password2'
        })
        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].help_text = 'Mínimo 8 caracteres. Apenas letras e números.'
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = 'Sua senha deve ter no mínimo 8 caracteres e conter números e letras.'
        self.fields['password2'].label = 'Confirme a senha'
        self.fields['password2'].help_text = 'Informe a mesma senha informada anteriormente.'
    
    def clean_username(self):
        """Sanitiza e valida o nome de usuário fornecido."""
        username = self.cleaned_data.get('username')
        if username:
            # Sanitiza o username
            username = bleach.clean(username, tags=[], strip=True)
            # Valida o formato
            validate_username_format(username)
        return username
    
    def clean_cpf(self):
        """Normaliza o CPF e garante que ele seja válido e único."""
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Sanitiza o CPF
            cpf = bleach.clean(cpf, tags=[], strip=True)
            # Remove caracteres não numéricos para validação e persistência
            cpf_numbers = re.sub(r'[^\d]', '', cpf)

            # Valida usando o algoritmo de CPF
            validate_cpf(cpf_numbers)

            # Verifica duplicidade independente de máscara
            pattern = r'^' + r'\D*'.join(cpf_numbers) + r'\D*$'
            if UserProfile.objects.filter(cpf__regex=pattern).exists():
                raise forms.ValidationError(
                    'Este CPF já está cadastrado. '
                    'Você pode fazer login ou recuperar sua conta.'
                )

            return cpf_numbers

        return cpf
    
    def clean_email(self):
        """Sanitiza o e-mail e confirma domínio e unicidade."""
        email = self.cleaned_data.get('email')
        if email:
            # Sanitiza o email
            email = bleach.clean(email, tags=[], strip=True).lower()
            # Valida caracteres permitidos
            validate_email_characters(email)
            # Valida domínios permitidos
            validate_allowed_email_domains(email)
            # Verifica se já está em uso
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    'Este e-mail já está cadastrado. '
                    'Você pode fazer login ou recuperar sua conta.'
                )
        return email
    
    def save(self, commit=True):
        """Persiste o usuário garantindo a sincronização com o perfil."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            cpf = self.cleaned_data.get('cpf')
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            user_profile.cpf = cpf
            user_profile.save()
            user.userprofile = user_profile
        return user
