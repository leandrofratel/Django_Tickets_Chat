from django.urls import path
from . import views
from .views import criar_sala_chat, room


urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('criar_sala/<int:ticket_id>/', criar_sala_chat, name='criar_sala_chat'),
    path('<slug:slug>/', room, name='room'),
]