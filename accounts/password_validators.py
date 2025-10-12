# accounts/password_validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    Validador de senha customizado que requer:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra (maiúscula OU minúscula)
    - Pelo menos 1 número
    - Pelo menos 1 símbolo
    """
    
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                'A senha deve ter no mínimo 8 caracteres.',
                code='password_too_short',
            )
        
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError(
                'A senha deve conter pelo menos uma letra.',
                code='password_no_letter',
            )
        
        if not re.search(r'\d', password):
            raise ValidationError(
                'A senha deve conter pelo menos um número.',
                code='password_no_number',
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/`~]', password):
            raise ValidationError(
                'A senha deve conter pelo menos um símbolo (!@#$%^&*(),.?":{}|<>_-+=[]\\;/`~).',
                code='password_no_symbol',
            )
    
    def get_help_text(self):
        return 'Sua senha deve ter no mínimo 8 caracteres e conter números, letras e símbolos.'
