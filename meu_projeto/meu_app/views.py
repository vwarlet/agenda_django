from django.shortcuts import render
from meu_app.models import Evento

# Create your views here.

def lista_eventos(request):
    # se eu quiser pegar os eventos do usuário logado
    #usuario = request.user
    #evento = Evento.objects.filter(usuario=usuario)
    evento = Evento.objects.all()
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

