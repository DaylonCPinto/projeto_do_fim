# Em accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Formulário de registro com validação de email e campos obrigatórios.
    """
    email = forms.EmailField(
        required=True,
        help_text='Obrigatório. Informe um endereço de email válido.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
    
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
        Salva o usuário com o email fornecido.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user