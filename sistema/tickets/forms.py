from django import forms
from django.contrib.auth.models import User
from .models import Ticket, TicketImage
from django.contrib.auth.forms import UserCreationForm

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'codigo_incidente', 'recurso', 'problema_apresentado',
            'link_alerta', 'link_itsm', 'grupo_suporte',
            'status', 'criticidade', 'responsavel'
        ]

        previsao = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Previsão em número'}))
        widgets = {
            'problema_apresentado': forms.Textarea(attrs={'rows': 1}),
        }

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'codigo_sx', 'acoes', 'solucao_contorno', 'causa_raiz',
            'status', 'grupo_suporte', 'analista','previsao'
        ]
        widgets = {
            'acoes': forms.Textarea(attrs={'rows': 3}),
            'solucao_contorno': forms.Textarea(attrs={'rows': 3}),
            'causa_raiz': forms.Textarea(attrs={'rows': 3}),
        }

class TicketImageForm(forms.ModelForm):
    class Meta:
        model = TicketImage
        fields = ['image']

#! Obsoleto
# class TicketFileForm(forms.ModelForm):
#     class Meta:
#         model = TicketFile
#         fields = ['file']

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']