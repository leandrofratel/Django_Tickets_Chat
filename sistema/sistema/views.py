from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def perfil(request):
    return render(request, 'perfil.html')

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após alterar a senha
            return redirect('perfil')  # Redireciona para o perfil após alterar a senha
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'alterar_senha.html', {'form': form})

# View para login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ticket_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# View para logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View para registro
def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para a página de login após registro
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# View para lista de tickets (apenas para usuários logados)
@login_required
def ticket_list(request):
    return render(request, 'ticket_list.html')
