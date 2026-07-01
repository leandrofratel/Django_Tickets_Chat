from .models import Room, Message
from tickets.models import Ticket
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def room(request, slug):
    """
    Exibe uma sala de bate-papo específica e suas mensagens.

    Args:
        request (HttpRequest): O objeto da requisição HTTP.
        slug (str): O identificador único da sala de bate-papo.

    Returns:
        HttpResponse: Renderiza a página 'chat/room.html' com o nome da sala e suas mensagens.
    """
    room_obj = get_object_or_404(Room, slug=slug)
    room_name = room_obj.name
    messages = Message.objects.filter(room=room_obj)
    
    return render(request, "chat/room.html", {"room_name": room_name, "slug": slug, 'messages': messages, 'room': room_obj})

@login_required
def criar_sala_chat(request, ticket_id):
    # Recupera o ticket com o ID fornecido. Se não existir, levanta Http404.
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Cria o nome e o slug da sala com base no número do incidente.
    sala_nome = f"{ticket.codigo_incidente}"
    sala_slug = slugify(f"{ticket.codigo_incidente}")

    # Cria a sala de chat associada ao ticket, se ainda não existir.
    room, created = Room.objects.get_or_create(
        ticket=ticket,
        defaults={'name': sala_nome, 'slug': sala_slug}
    )

    # Verifica se a sala foi criada ou já existia.
    if created:
        print(f"Sala criada: {sala_nome} com slug {sala_slug}")
    else:
        print(f"A sala já existe para o ticket: {sala_nome}")

    return redirect('room', slug=room.slug)
