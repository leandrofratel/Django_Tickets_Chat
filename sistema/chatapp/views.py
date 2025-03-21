from django.shortcuts import render
from .models import Room,Message

def rooms(request):
    """
    Exibe a lista de todas as salas de bate-papo disponíveis.

    Args:
        request (HttpRequest): O objeto da requisição HTTP.

    Returns:
        HttpResponse: Renderiza a página 'chat/rooms.html' com a lista de salas.
    """
    rooms=Room.objects.all()
    return render(request, "chat/rooms.html",{"rooms":rooms})

def room(request,slug):
    """
    Exibe uma sala de bate-papo específica e suas mensagens.

    Args:
        request (HttpRequest): O objeto da requisição HTTP.
        slug (str): O identificador único da sala de bate-papo.

    Returns:
        HttpResponse: Renderiza a página 'chat/room.html' com o nome da sala e suas mensagens.
    """
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request, "chat/room.html",{"room_name":room_name, "slug":slug, 'messages':messages})