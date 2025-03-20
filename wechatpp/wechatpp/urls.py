from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',include('chatapp.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('tickets',include('tickets.urls')),
]
