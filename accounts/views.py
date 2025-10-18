# Em accounts/views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import SignUpForm, EmailAuthenticationForm


@csrf_protect
@never_cache
def signup(request):
    """
    View para registro de novos usuários.
    Protegido contra CSRF e não permite cache.
    """
    # Redireciona usuários já autenticados
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Login automático após registro - specify backend
            login(request, user, backend='accounts.backends.EmailAuthenticationBackend')
            messages.success(request, 'Conta criada com sucesso! Bem-vindo!')
            return redirect('welcome')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {
        'form': form,
        'title': 'Criar Conta'
    })


@never_cache
def welcome(request):
    """
    View para página de boas-vindas após registro.
    Requer autenticação.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'registration/welcome.html', {
        'title': 'Bem-vindo'
    })


@csrf_protect
@never_cache
def custom_login(request):
    """
    View customizada para login usando e-mail.
    """
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo de volta, {user.username}!')
            # Redireciona para a próxima página ou home com validação segura
            next_url = request.GET.get('next') or request.POST.get('next')
            fallback_url = settings.LOGIN_REDIRECT_URL or '/'
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host(), *settings.ALLOWED_HOSTS},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect(fallback_url)
        else:
            messages.error(request, 'E-mail ou senha incorretos.')
    else:
        form = EmailAuthenticationForm()
    
    return render(request, 'registration/login.html', {
        'form': form,
        'title': 'Login'
    })

