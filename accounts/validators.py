# accounts/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_cpf(cpf):
    """
    Valida CPF usando o algoritmo de verificação dos dígitos.
    """
    # Remove caracteres não numéricos
    cpf_numbers = re.sub(r'[^\d]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_numbers) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.')
    
    # Verifica se não é uma sequência repetida
    if cpf_numbers == cpf_numbers[0] * 11:
        raise ValidationError('CPF inválido.')
    
    # Validação dos dígitos verificadores
    def calculate_digit(cpf_partial, weights):
        total = sum(int(digit) * weight for digit, weight in zip(cpf_partial, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # Primeiro dígito verificador
    first_digit = calculate_digit(cpf_numbers[:9], range(10, 1, -1))
    if int(cpf_numbers[9]) != first_digit:
        raise ValidationError('CPF inválido.')
    
    # Segundo dígito verificador
    second_digit = calculate_digit(cpf_numbers[:10], range(11, 1, -1))
    if int(cpf_numbers[10]) != second_digit:
        raise ValidationError('CPF inválido.')
    
    return cpf


def validate_allowed_email_domains(email):
    """
    Valida se o email usa um dos domínios permitidos.
    """
    allowed_domains = ['@gmail.com', '@outlook.com', '@hotmail.com']
    email_lower = email.lower()
    
    if not any(email_lower.endswith(domain) for domain in allowed_domains):
        raise ValidationError(
            'Somente e-mails com os domínios @gmail.com, @outlook.com e @hotmail.com são aceitos.'
        )
    
    return email


def validate_username_format(username):
    """
    Valida formato do nome de usuário:
    - Mínimo 8 caracteres
    - Apenas letras e números
    - Pelo menos uma letra
    """
    if len(username) < 8:
        raise ValidationError('O nome de usuário deve ter no mínimo 8 caracteres.')
    
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        raise ValidationError('O nome de usuário pode conter apenas letras e números.')
    
    if not re.search(r'[a-zA-Z]', username):
        raise ValidationError('O nome de usuário deve conter pelo menos uma letra.')
    
    return username


def validate_email_characters(email):
    """
    Valida que o email contém apenas caracteres permitidos antes do @.
    Permitidos: letras, números, ".", "-", "_"
    """
    local_part = email.split('@')[0] if '@' in email else email
    
    if not re.match(r'^[a-zA-Z0-9._-]+$', local_part):
        raise ValidationError(
            'O e-mail pode conter apenas letras, números, pontos (.), hífens (-) e underscores (_).'
        )
    
    return email
