from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import SignUpForm
from .validators import (
    validate_cpf,
    validate_allowed_email_domains,
    validate_username_format,
    validate_email_characters
)


class CPFValidatorTest(TestCase):
    """Tests for CPF validation"""
    
    def test_valid_cpf(self):
        """Test with a valid CPF"""
        # CPF válido: 111.444.777-35
        try:
            validate_cpf('111.444.777-35')
        except ValidationError:
            self.fail('validate_cpf raised ValidationError unexpectedly!')
    
    def test_invalid_cpf_repeated_digits(self):
        """Test CPF with all same digits"""
        with self.assertRaises(ValidationError):
            validate_cpf('111.111.111-11')
    
    def test_invalid_cpf_wrong_digits(self):
        """Test CPF with wrong verification digits"""
        with self.assertRaises(ValidationError):
            validate_cpf('123.456.789-00')
    
    def test_invalid_cpf_too_short(self):
        """Test CPF with less than 11 digits"""
        with self.assertRaises(ValidationError):
            validate_cpf('123.456.789')


class EmailValidatorTest(TestCase):
    """Tests for email validation"""
    
    def test_valid_gmail(self):
        """Test valid Gmail address"""
        try:
            validate_allowed_email_domains('user@gmail.com')
        except ValidationError:
            self.fail('validate_allowed_email_domains raised ValidationError unexpectedly!')
    
    def test_valid_outlook(self):
        """Test valid Outlook address"""
        try:
            validate_allowed_email_domains('user@outlook.com')
        except ValidationError:
            self.fail('validate_allowed_email_domains raised ValidationError unexpectedly!')
    
    def test_invalid_outlook_br(self):
        """Test that Outlook.com.br is no longer accepted"""
        with self.assertRaises(ValidationError):
            validate_allowed_email_domains('user@outlook.com.br')
    
    def test_valid_hotmail(self):
        """Test valid Hotmail address"""
        try:
            validate_allowed_email_domains('user@hotmail.com')
        except ValidationError:
            self.fail('validate_allowed_email_domains raised ValidationError unexpectedly!')
    
    def test_invalid_domain(self):
        """Test email with invalid domain"""
        with self.assertRaises(ValidationError):
            validate_allowed_email_domains('user@yahoo.com')
    
    def test_email_characters_valid(self):
        """Test email with valid characters"""
        try:
            validate_email_characters('user.name_test-123@gmail.com')
        except ValidationError:
            self.fail('validate_email_characters raised ValidationError unexpectedly!')
    
    def test_email_characters_invalid(self):
        """Test email with invalid characters"""
        with self.assertRaises(ValidationError):
            validate_email_characters('user#name@gmail.com')


class UsernameValidatorTest(TestCase):
    """Tests for username validation"""
    
    def test_valid_username(self):
        """Test valid username"""
        try:
            validate_username_format('username123')
        except ValidationError:
            self.fail('validate_username_format raised ValidationError unexpectedly!')
    
    def test_username_too_short(self):
        """Test username with less than 8 characters"""
        with self.assertRaises(ValidationError):
            validate_username_format('user123')
    
    def test_username_with_special_chars(self):
        """Test username with special characters"""
        with self.assertRaises(ValidationError):
            validate_username_format('user@name123')
    
    def test_username_only_numbers(self):
        """Test username with only numbers"""
        with self.assertRaises(ValidationError):
            validate_username_format('12345678')


class SignUpFormTest(TestCase):
    """Tests for SignUpForm"""
    
    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'username': 'testuser123',
            'email': 'test@gmail.com',
            'cpf': '111.444.777-35',
            'password1': 'SecurePass456',
            'password2': 'SecurePass456',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_form_invalid_email_domain(self):
        """Test form with invalid email domain"""
        form_data = {
            'username': 'testuser123',
            'email': 'test@yahoo.com',
            'cpf': '111.444.777-35',
            'password1': 'SecurePass456',
            'password2': 'SecurePass456',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_invalid_username_too_short(self):
        """Test form with username too short"""
        form_data = {
            'username': 'test',
            'email': 'test@gmail.com',
            'cpf': '111.444.777-35',
            'password1': 'SecurePass456',
            'password2': 'SecurePass456',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_form_invalid_cpf(self):
        """Test form with invalid CPF"""
        form_data = {
            'username': 'testuser123',
            'email': 'test@gmail.com',
            'cpf': '123.456.789-00',
            'password1': 'SecurePass456',
            'password2': 'SecurePass456',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cpf', form.errors)
    
    def test_form_password_valid_without_symbol(self):
        """Test form with password without symbol (now valid)"""
        form_data = {
            'username': 'johnsmith99',
            'email': 'test@gmail.com',
            'cpf': '111.444.777-35',
            'password1': 'ValidPass456',
            'password2': 'ValidPass456',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
    
    def test_form_duplicate_email(self):
        """Test form with duplicate email"""
        # Create a user first
        User.objects.create_user(
            username='existinguser',
            email='test@gmail.com',
            password='SecurePass456'
        )
        
        form_data = {
            'username': 'testuser123',
            'email': 'test@gmail.com',
            'cpf': '111.444.777-35',
            'password1': 'SecurePass456',
            'password2': 'SecurePass456',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
