from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from .models import Ticket, TicketImage
from .forms import TicketForm, TicketUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

def tempo_decorrido(request, pk):
    """
    Retorna o tempo decorrido de um ticket em formato JSON.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    tempo = ticket.tempo_corrente()
    return JsonResponse({'tempo_decorrido': tempo})

def ticket_registro(request):
    """
    Permite a criação de novos usuários. Solicita:
    - Nome
    - Senha
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) ## Loga o user automaticamente
            messages.success(request, "Conta criada com sucesso!")
            return redirect("ticket_meus_incidentes")
        form = UserCreationForm()
    return render(request, "registration/registro.html", {"form": form})

@login_required
def ticket_list(request):
    """ Lista todos os tickets cadastrados no sistema. """
    tickets = Ticket.objects.exclude(status="Fechado")
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets
    })

@login_required
def ticket_archive(request):
    """ Lista todos os tickets Fechados do sistema. """
    tickets = Ticket.objects.filter(status="Fechado")
    return render(request, 'tickets/ticket_archive.html', {
        'tickets': tickets
    })

@login_required
def ticket_meus_incidentes(request): 
    """ Lista todos os tickets do usuário logado. """
    tickets = Ticket.objects.filter(analista=request.user.username)
    return render(request, 'tickets/ticket_meus_incidentes.html', {
        'tickets': tickets
    })

@login_required
def ticket_create(request):
    """
    - Se a requisição for POST, 
        valida e salva o ticket, além de processar o upload de imagens.
    - Se a requisição for GET, 
        exibe o formulário vazio para criação de um novo ticket.
    """
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save() # Salva o ticket

            #* Processa as imagens
            for file in request.FILES.getlist('images'):
                TicketImage.objects.create(ticket=ticket, image=file)

            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_update(request, pk):
    """
    - Se a requisição for POST, valida e atualiza o ticket, 
        além de processar o upload de novas imagens.
    - Se a requisição for GET, 
        exibe o formulário preenchido com os dados do ticket para edição.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        update_form = TicketUpdateForm(request.POST, instance=ticket)
        if update_form.is_valid():
            nova_acao = update_form.cleaned_data.get('nova_acao')
            if nova_acao:
                ticket.adicionar_acao(nova_acao, request.user)
            
            update_form.save()
            
            # Processamento de imagens (mantido igual)
            for file in request.FILES.getlist('images'):
                TicketImage.objects.create(ticket=ticket, image=file)
                
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        update_form = TicketUpdateForm(instance=ticket)
    
    return render(request, 'tickets/ticket_update_form.html', {
        'form': update_form, 
        'ticket': ticket
    })

@login_required
def ticket_delete(request, pk):
    """
    Exclui um ticket existente.
    - Se a requisição for POST, exclui o ticket do banco de dados.
    - Se a requisição for GET, 
    exibe uma página de confirmação para exclusão do ticket.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')
    return render(request, 'tickets/ticket_confirm_delete.html', {'ticket': ticket})

@login_required
def ticket_detail(request, pk):
    """
    Exibe os detalhes de um ticket específico.
    - Recupera um ticket com base no pk (chave primária)
    e exibe suas informações.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
def ticket_dashboard(request):
    """
    Apresenta a tela principal de Dashboard com os indicadores abaixo.
    - Status dos Incidentes;
    - Quantidade de Incidentes por Criticidade
    """

    # Recupera o total de incidentes.
    tickets = Ticket.objects.all().order_by('-criado_em')[:11]
    total_incidentes = Ticket.objects.count()

    # Quantidade de incidentes por status.
    incidentes_fechados = Ticket.objects.filter(status='Fechado').count()
    incidentes_resolvidos = Ticket.objects.filter(status='Resolvido').count()
    incidentes_andamento = Ticket.objects.filter(status='Em Andamento').count()
    incidentes_analise = Ticket.objects.filter(status='Em Análise').count()

    # Criticidade
    inc_crit_alta = Ticket.objects.filter(criticidade="Alta")\
        .count()
    inc_crit_media = Ticket.objects.filter(criticidade="Média")\
        .count()
    inc_crit_baixa = Ticket.objects.filter(criticidade="Baixa").count()

    # Passa as informações para o template
    context = {
        'total_incidentes': total_incidentes,
        'incidentes_fechados': incidentes_fechados,
        'incidentes_resolvidos': incidentes_resolvidos,
        'incidentes_andamento': incidentes_andamento,
        'incidentes_analise': incidentes_analise,

        # Criticidade
        'inc_crit_alta':inc_crit_alta,
        'inc_crit_media':inc_crit_media,
        'inc_crit_baixa':inc_crit_baixa,

        'tickets': tickets
    }

    return render(request, 'tickets/ticket_dashboard.html', context)
