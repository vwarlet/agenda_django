from django.shortcuts import render, redirect
from meu_app.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from datetime import datetime, timedelta


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
    return redirect('/')    

@login_required(login_url='/login/')
def lista_eventos(request):
    # mostra apenas os eventos do usuario logado
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario) 
        # se eu adicionar ao filtro (data_atual__gt=data_atual), exibirá só os próximos eventos
        # e (data_atual__lt=data_atual), exibe só os eventos que já passaram
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        '''
        # outro modo de fazer as alterações
        evento = Evento.objects.get(id=id_evento)
        if evento.usuario == usuario:
            evento.titulo = titulo
            evento.descricao = descricao
            evento.data_evento = data_evento
            evento.save()
        '''
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo = titulo, data_evento = data_evento, descricao = descricao)
        else: 
            Evento.objects.create(titulo = titulo, data_evento = data_evento, descricao = descricao, usuario = usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    # usuario logado só pode excluir os seus eventos
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')

def json_lista_eventos(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo', 'data_evento', 'descricao')
    return JsonResponse(list(evento), safe=False)
