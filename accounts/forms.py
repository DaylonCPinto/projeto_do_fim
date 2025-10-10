# Em accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
import re


class SignUpForm(UserCreationForm):
    """
    Formulário de registro com validação de email, CPF e campos obrigatórios.
    """
    email = forms.EmailField(
        required=True,
        label='E-mail',
        help_text='Obrigatório. Informe um endereço de email válido.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    cpf = forms.CharField(
        max_length=14,
        required=True,
        label='CPF',
        help_text='Informe o CPF no formato: XXX.XXX.XXX-XX',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '000.000.000-00'
        })
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'cpf', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Nome de usuário'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirme a senha'
    
    def clean_cpf(self):
        """
        Valida o formato do CPF.
        """
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf_numbers = re.sub(r'[^\d]', '', cpf)
            
            # Verifica se tem 11 dígitos
            if len(cpf_numbers) != 11:
                raise forms.ValidationError('CPF deve conter 11 dígitos.')
            
            # Verifica se não é uma sequência repetida
            if cpf_numbers == cpf_numbers[0] * 11:
                raise forms.ValidationError('CPF inválido.')
            
            # Verifica se o CPF já está em uso
            if UserProfile.objects.filter(cpf=cpf).exists():
                raise forms.ValidationError('Este CPF já está cadastrado.')
        
        return cpf
    
    def clean_email(self):
        """
        Valida que o email não está sendo usado por outro usuário.
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está sendo usado.')
        return email
    
    def save(self, commit=True):
        """
        Salva o usuário com o email e CPF fornecidos.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Atualiza o perfil com o CPF
            if hasattr(user, 'userprofile'):
                user.userprofile.cpf = self.cleaned_data.get('cpf')
                user.userprofile.save()
        return user