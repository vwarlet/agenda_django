from django.shortcuts import render, redirect
from meu_app.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido!")
    redirect('/')    

@login_required(login_url='/login/')
def lista_eventos(request):
    # mostra apenas os eventos do usuario logado
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

