from .forms import PerfilForm
from django.http import JsonResponse
from django.contrib import messages
from .forms import TicketForm, TicketUpdateForm
from .models import Ticket, TicketImage, TicketFile
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def tempo_decorrido(request, pk):
    """
    Retorna o tempo decorrido de um ticket em formato JSON.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    tempo = ticket.tempo_corrente()  # Chama o método que calcula o tempo decorrido
    return JsonResponse({'tempo_decorrido': tempo})

@login_required
def ticket_list(request): #? Exibe a lista de incidentes cadastrados
    """ Lista todos os tickets cadastrados no sistema. """
    # tickets = Ticket.objects.all()
    tickets = Ticket.objects.exclude(status="Fechado")
    return render(request, 'tickets/ticket_list.html', {
        'tickets': tickets
    })

@login_required
def ticket_archive(request): #? Existe todos os incidentes Fechados/ Arquivados
    """ Lista todos os tickets Fechados do sistema. """
    tickets = Ticket.objects.filter(status="Fechado")
    return render(request, 'tickets/ticket_archive.html', {
        'tickets': tickets
    })

@login_required
def ticket_create(request): #? Cria um novo Incidente
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

            #* Processa os arquivos
            for file in request.FILES.getlist('files'):
                TicketFile.objects.create(ticket=ticket, file=file)

            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_update(request, pk): #? Atualiza um Incidente
    """
    - Se a requisição for POST, valida e atualiza o ticket, 
        além de processar o upload de novas imagens.
    - Se a requisição for GET, 
        exibe o formulário preenchido com os dados do ticket para edição.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        update_form = TicketUpdateForm(
            request.POST, request.FILES, instance=ticket
        )
        if update_form.is_valid():
            ticket = update_form.save() # Salva as alterações do ticket

            # Processa as novas imagens
            for file in request.FILES.getlist('images'):
                TicketImage.objects.create(ticket=ticket, image=file)

            # Processa as novos arquivos
            for file in request.FILES.getlist('files'):
                TicketImage.objects.create(ticket=ticket, file=file)
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        update_form = TicketUpdateForm(instance=ticket)
    return render(request, 'tickets/ticket_update_form.html', {
        'form': update_form, 'ticket': ticket
    })

@login_required
def ticket_delete(request, pk): #? Deleta um Incidente
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
def ticket_detail(request, pk): #? Permite visualizar detalhes do incidente
    """
    Exibe os detalhes de um ticket específico.
    - Recupera um ticket com base no pk (chave primária)
    e exibe suas informações.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
def ticket_dashboard(request): #? Dahsboard com os indicadores
    """
    Apresenta a tela principal de Dashboard com os indicadores abaixo.
    - Status dos Incidentes;
    - Quantidade de Incidentes por Criticidade
    """

    # Recupera o total de incidentes.
    tickets = Ticket.objects.all().order_by('-criado_em')[:11]
    total_incidentes = Ticket.objects.count()

    # Quantidade de incidentes por status.
    incidentes_abertos = Ticket.objects.filter(status='Aberto').count()
    incidentes_fechados = Ticket.objects.filter(status='Fechado').count()
    incidentes_resolvidos = Ticket.objects.filter(status='Resolvido').count()
    incidentes_andamento = Ticket.objects.filter(status='Em Andamento').count()
    incidentes_analise = Ticket.objects.filter(status='Em Análise').count()
    incidentes_crise = Ticket.objects.filter(status='Sala de Crise').count()

    # Criticidade
    inc_hiper_criticos = Ticket.objects.filter(criticidade="Hiper Crítico")\
        .count()
    inc_muito_criticos = Ticket.objects.filter(criticidade="Muito Crítico")\
        .count()
    inc_criticos = Ticket.objects.filter(criticidade="Crítico").count()

    # Passa as informações para o template
    context = {
        'total_incidentes': total_incidentes,
        'incidentes_abertos': incidentes_abertos,
        'incidentes_fechados': incidentes_fechados,
        'incidentes_resolvidos': incidentes_resolvidos,
        'incidentes_andamento': incidentes_andamento,
        'incidentes_analise': incidentes_analise,
        'incidentes_crise': incidentes_crise,

        # Criticidade
        'inc_hiper_criticos':inc_hiper_criticos,
        'inc_muito_criticos':inc_muito_criticos,
        'inc_criticos':inc_criticos,

        'tickets': tickets
    }

    return render(request, 'tickets/ticket_dashboard.html', context)

@login_required
def ticket_registro(request):
    """
    Permite a criação de novos usuários.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login para continuar.")
            return redirect("login")  # Redireciona para a página de login
    else:
        form = UserCreationForm()

    return render(request, "registration/registro.html", {"form": form})

@login_required
def perfil(request):
    """
    Tela de perfil de usuário
    """
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'registration/perfil.html', {'form': form})