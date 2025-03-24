from django.urls import path
from . import views
from .views import criar_sala_chat


urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),

    #! Novas Rotas
    path('criar_sala/<int:ticket_id>/', criar_sala_chat, name='criar_sala_chat'),
]