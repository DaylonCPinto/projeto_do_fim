# Em accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from .forms import SignUpForm


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
            # Login automático após registro
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo!')
            return redirect('/')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {
        'form': form,
        'title': 'Criar Conta'
    })