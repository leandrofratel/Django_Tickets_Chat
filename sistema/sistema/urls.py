from django.contrib import admin
from django.urls import path, include
from tickets.views import ticket_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    ## Página Principal
    path('', ticket_dashboard, name='home'),

    ## Demais urls
    path('chat/', include('chatapp.urls')),
    path('tickets/', include('tickets.urls')),
]
