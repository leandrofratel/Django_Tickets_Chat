from .views import logout_view, login_view, registro_view, perfil, alterar_senha
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from tickets.views import ticket_dashboard
from django.conf import settings
from django.conf.urls.static import static

def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', home_redirect),
    path('admin/', admin.site.urls),

    ## Login
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("registro/", registro_view, name="registro"),
    path("perfil/", perfil, name="perfil"),
    path("alterar_senha/", alterar_senha, name="alterar_senha"),

    ## Página Principal
    path('', ticket_dashboard, name='home'),

    ## Apps
    path('chat/', include('chatapp.urls')),
    path('tickets/', include('tickets.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)