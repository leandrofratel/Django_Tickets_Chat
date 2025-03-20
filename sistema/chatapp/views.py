from django.shortcuts import render
from .models import Room,Message

def rooms(request):
    rooms=Room.objects.all()
    return render(request, "chat/rooms.html",{"rooms":rooms})

def room(request,slug):
    room_name=Room.objects.get(slug=slug).name
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request, "chat/room.html",{"room_name":room_name, "slug":slug, 'messages':messages})