from django.db import models
from django.utils.timezone import now

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Fechado', 'Fechado'),
        ('Resolvido', 'Resolvido'),
        ('Em Andamento', 'Em Andamento'),
        ('Designado', 'Designado'),
        ('Em Análise', 'Em Análise'),
        ('Sala de Crise', 'Sala de Crise'),
    ]

    SUPORTE_CHOICES = [
        ('COI - Grupo de Operações Integradas','COI - Grupo de Operações Integradas'),
        ('COI - Gestão de Problemas', 'COI - Gestão de Problemas'),
        ('Operações IBM','Operações IBM'),
    ]

    ANALISTAS_CHOICES = [
        ('Leandro Fratel','Leandro Fratel'),
        ('Heráclito Teixeira','Heráclito Teixeira'),
        ('Camilla Gama','Camilla Gama'),
    ]

    RECURSO_CRITICIDADE_MAP = {
        'Balcão Único':'Hiper Crítico',
        'Plataforma REDE SP.GOV.BR':'Hiper Crítico',
        'Central de Transplantes':'Hiper Crítico',
        'CNH':'Hiper Crítico',
        'CRV':'Hiper Crítico',
        'Portal Detran':'Hiper Crítico',
        'Portal Poupatempo':'Hiper Crítico',
        'Prova Eletrônica':'Hiper Crítico',
        'SEI':'Hiper Crítico',
        'TOTEM':'Hiper Crítico',
        
        'Agendamento Universal - Agenda SP':'Muito Crítico',
        'CAR - Cadastro de Atendimento e Relacionamento':'Muito Crítico',
        'Delegacia Eletrônica':'Muito Crítico',
        'e-Vistoria':'Muito Crítico',
        'Multas DER':'Muito Crítico',
        'Poupafila Centralizado':'Muito Crítico',
        'SIM':'Muito Crítico',
        'SPJ':'Muito Crítico',

        'Aplicações Mobile':'Crítico',
        'Detecta':'Crítico',
        'Inquérito Eletrônico':'Crítico',
        'Ipva Online':'Crítico',
        'Rede Palácio do Governo':'Crítico',
        'S4SP':'Crítico',
        'Sistema Alpha':'Crítico',
        'Valid - IIRGD':'Crítico',
    }

    RECURSO_RESPONSAVEL_MAP = {
        'Balcão Único':'Tiago Pretel dos Santos',
        'Plataforma REDE SP.GOV.BR':'Paulo Ambrozevicius Junior',
        'Central de Transplantes':'David Francisco Ramos',
        'CNH':'Andreia Lopes Macedo Salaroli',
        'CRV':'Eric Daniel David',
        'Portal Detran':'Tiago Pretel dos Santos',
        'Portal Poupatempo':'Tiago Pretel dos Santos',
        'Prova Eletrônica':'Andreia Lopes Macedo Salaroli',
        'SEI':'Deise Kusunoki Shirozono',
        'TOTEM':'Emanuel Henrique Ferreira de Campos',

        'Agendamento Universal - Agenda SP':'Tiago Pretel dos Santos',
        'CAR - Cadastro de Atendimento e Relacionamento':'Sérgio Sotero Dafonte Tavares',
        'Delegacia Eletrônica':'Demis de Fiore',
        'e-Vistoria':'Eric Daniel David',
        'Multas DER':'Ricardo Pereira',
        'Poupafila Centralizado':'Tiago Pretel dos Santos',
        'SIM':'Celso Soares do Nascimento',
        'SPJ':'Sidney Morilhas',

        'Aplicações Mobile':'Andrea Mihee Jin',
        'Detecta':'Cristiano da Silva Xavier',
        'Inquérito Eletrônico':'Sidney Morilhas',
        'Ipva Online':'Izilda Cristina Furlan de Faria Freitas',
        'Rede Palácio do Governo':'Camila Pereira',
        'S4SP':'Marcelo Fernandes Garcez',
        'Sistema Alpha':'Graziella Pica de Lucca',
        'Valid - IIRGD':'Graziella Pica de Lucca',
    }

    RECURSOS_CHOICES = [
        ('Balcão Único', 'Balcão Único'),
        ('Central de Transplantes', 'Central de Transplantes'),
        ('CNH', 'CNH'),
        ('CRV', 'CRV'),
        ('Plataforma REDE SP.GOV.BR', 'Plataforma REDE SP.GOV.BR'),
        ('Portal Detran', 'Portal Detran'),
        ('Portal Poupatempo', 'Portal Poupatempo'),
        ('Prova Eletrônica', 'Prova Eletrônica'),
        ('SEI', 'SEI'),
        ('TOTEM', 'TOTEM'),
        ('Agendamento Universal - Agenda SP', 'Agendamento Universal - Agenda SP'),
        ('CAR - Cadastro de Atendimento e Relacionamento', 'CAR - Cadastro de Atendimento e Relacionamento'),
        ('Delegacia Eletrônica', 'Delegacia Eletrônica'),
        ('e-Vistoria', 'e-Vistoria'),
        ('Multas DER', 'Multas DER'),
        ('Poupafila Centralizado', 'Poupafila Centralizado'),
        ('SIM', 'SIM'),
        ('SPJ', 'SPJ'),
        ('Aplicações Mobile', 'Aplicações Mobile'),
        ('Detecta', 'Detecta'),
        ('Inquérito Eletrônico', 'Inquérito Eletrônico'),
        ('Ipva Online', 'Ipva Online'),
        ('Rede Palácio do Governo', 'Rede Palácio do Governo'),
        ('S4SP', 'S4SP'),
        ('Sistema Alpha', 'Sistema Alpha'),
        ('Valid - IIRGD', 'Valid - IIRGD')
    ]

    # Identificadores
    codigo_incidente = models.CharField(max_length=50, verbose_name="Incidente")
    codigo_sx = models.CharField(max_length=50, verbose_name="SX", default="", blank=True)
    recurso = models.CharField(max_length=50, verbose_name="Recurso", choices=RECURSOS_CHOICES)

    # Caixas de Texto
    problema_apresentado = models.CharField(max_length=50, verbose_name="Problema Apresentado")
    acoes = models.TextField(verbose_name="Ações") #TODO: REMOVER ESTA LINHA
    solucao_contorno = models.TextField(verbose_name="Solução de Contorno")
    causa_raiz = models.TextField(verbose_name="Causa Raiz")

    # Links
    link_alerta = models.URLField(verbose_name="Alerta Dynatrace", blank=True, null=True)
    link_itsm = models.URLField(verbose_name="Link do Incidente ITSM", blank=True, null=True)

    # Choises
    grupo_suporte = models.CharField(
        max_length=100,
        choices=SUPORTE_CHOICES, default='',
        verbose_name="Grupo de Suporte"
    )
    responsavel = models.CharField(
        max_length=100,
        verbose_name="Responsável",
        editable=False
    )
    analista = models.CharField(
        max_length=100, 
        choices=ANALISTAS_CHOICES, 
        default='Não Atribuido', 
        verbose_name="Analista"
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='Aberto', 
        verbose_name="Status"
    )
    criticidade = models.CharField(
        max_length=50, 
        choices='', 
        default='Crítico', 
        verbose_name="Criticidade",
        editable=False
    )

    # Campos de Data
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    fechado_em = models.DateTimeField(null=True, blank=True)
    previsao = models.IntegerField(null=True, blank=True, verbose_name="Previsão em minutos")

    def tempo_corrente(self):
        """
        Retorna o tempo total em aberto em minutos (inteiro).
        """
        if self.fechado_em:
            return round((self.fechado_em - self.criado_em).total_seconds() / 60)
        return round((now() - self.criado_em).total_seconds() / 60)

    def save(self, *args, **kwargs):
        """ Para a contagem de tempo apenas quando o status for 'Fechado' ou 'Resolvido' """
        if self.status in ['Fechado', 'Resolvido'] and not self.fechado_em:
            self.fechado_em = now()  # Registra o horário de fechamento

        ## Criticidade com base no recurso selecionado
        if self.recurso in self.RECURSO_CRITICIDADE_MAP:
            self.criticidade = self.RECURSO_CRITICIDADE_MAP[self.recurso]

        ## Criticidade com base no recurso selecionado
        if self.recurso in self.RECURSO_RESPONSAVEL_MAP:
            self.responsavel = self.RECURSO_RESPONSAVEL_MAP[self.recurso]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_incidente} - {self.responsavel}"

class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tickets/images/')

    def __str__(self):
        return f"Imagem do Ticket {self.ticket.codigo_incidente}"