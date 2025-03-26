from django import forms
from .models import Ticket, TicketImage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'codigo_incidente', 'recurso', 'problema_apresentado',
            'link_alerta', 'link_itsm', 'grupo_suporte',
            'status'
        ]

        previsao = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Previsão em número'}))

class TicketUpdateForm(forms.ModelForm):
    nova_acao = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':4}),
        label="Ação Realizada"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['solucao_contorno'].required = False

    class Meta:
        model = Ticket
        fields = [
            'codigo_sx', 'status',
            'grupo_suporte', 'analista',
            'previsao', 'solucao_contorno'
        ]
        widgets = {
            'solucao_contorno': forms.Textarea(attrs={'rows': 4}),
        }

class TicketImageForm(forms.ModelForm):
    class Meta:
        model = TicketImage
        fields = ['image']

class PerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']

class RegistroForm(UserCreationForm):
    """
    """
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
