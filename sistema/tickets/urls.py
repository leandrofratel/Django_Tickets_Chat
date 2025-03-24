from . import views
from django.urls import path

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('novo/', views.ticket_create, name='ticket_create'),
    path('editar/<int:pk>/', views.ticket_update, name='ticket_update'),
    path('excluir/<int:pk>/', views.ticket_delete, name='ticket_delete'),
    path('detalhes/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('dashboard/', views.ticket_dashboard, name='ticket_dashboard'),
    path('registro/', views.ticket_registro, name='ticket_registro'),
    path('arquivado/', views.ticket_archive, name='ticket_archive'),
    path('ticket_gestao_problemas/', views.ticket_gestao_problemas, name='ticket_gestao_problemas'),
    path('tempo_decorrido/<int:pk>/', views.tempo_decorrido, name='tempo_decorrido'),
]