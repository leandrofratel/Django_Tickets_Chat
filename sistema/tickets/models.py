from django.db import models
from django.utils.timezone import now, localtime
from django.contrib.auth.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Em Andamento', 'Em Andamento'),
        ('Fechado', 'Fechado'),
        ('Resolvido', 'Resolvido'),
        ('Em Análise', 'Em Análise'),
    ]
    SUPORTE_CHOICES = [
        ('COI - Grupo de Operações Integradas','COI - Grupo de Operações Integradas'),
        ('COI - Gestão de Problemas', 'COI - Gestão de Problemas'),
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
        ('Agendamento Universal - Agenda SP', 'Agendamento Universal - Agenda SP'),
        ('Aplicações Mobile', 'Aplicações Mobile'),
        ('Balcão Único', 'Balcão Único'),
        ('CAR - Cadastro de Atendimento e Relacionamento', 'CAR - Cadastro de Atendimento e Relacionamento'),
        ('Central de Transplantes', 'Central de Transplantes'),
        ('Certificação Digital', 'Certificação Digital'),
        ('CNH', 'CNH'),
        ('CRV', 'CRV'),
        ('Delegacia Eletrônica', 'Delegacia Eletrônica'),
        ('Detecta', 'Detecta'),
        ('e-Vistoria', 'e-Vistoria'),
        ('Inquérito Eletrônico', 'Inquérito Eletrônico'),
        ('Ipva Online', 'Ipva Online'),
        ('Multas DER', 'Multas DER'),
        ('Plataforma REDE SP.GOV.BR', 'Plataforma REDE SP.GOV.BR'),
        ('Portal Detran', 'Portal Detran'),
        ('Portal Poupatempo', 'Portal Poupatempo'),
        ('Poupafila Centralizado', 'Poupafila Centralizado'),
        ('Prova Eletrônica', 'Prova Eletrônica'),
        ('Rede Palácio do Governo', 'Rede Palácio do Governo'),
        ('S4SP', 'S4SP'),
        ('SEI', 'SEI'),
        ('SIM', 'SIM'),
        ('Sistema Alpha', 'Sistema Alpha'),
        ('SPJ', 'SPJ'),
        ('TOTEM', 'TOTEM'),
        ('Valid - IIRGD', 'Valid - IIRGD')
    ]

    # Identificadores do Incidente
    codigo_incidente = models.CharField(max_length=50, verbose_name="Incidente", unique=True)
    codigo_sx = models.CharField(max_length=50, verbose_name="SX", default="", blank=True)
    recurso = models.CharField(max_length=50, verbose_name="Recurso", choices=RECURSOS_CHOICES)
    problema_apresentado = models.CharField(max_length=200, verbose_name="Problema Apresentado")
    analista = models.CharField(max_length=100, default="", verbose_name="Analista", blank=True, null=True)

    # Caixas de Texto livre
    historico_acoes = models.TextField(verbose_name="Histórico de Ações", blank=True, editable=False)
    solucao_contorno = models.TextField(verbose_name="Solução de Contorno", blank=True, null=True, default="")

    # Links de Acesso
    link_alerta = models.URLField(verbose_name="Link alerta Dynatrace", blank=True, null=True, default="")
    link_itsm = models.URLField(verbose_name="Link do Incidente ITSM", blank=True, null=True, default="")

    # Campos de Escolha
    grupo_suporte = models.CharField(max_length=100,choices=SUPORTE_CHOICES, verbose_name="Grupo de Suporte")
    responsavel = models.CharField(max_length=100, verbose_name="Responsável", editable=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Aberto', verbose_name="Status")
    criticidade = models.CharField(max_length=50, verbose_name="Criticidade", editable=False)

    # Campos de Data
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    fechado_em = models.DateTimeField(null=True, blank=True)
    previsao = models.IntegerField(null=True, blank=True, verbose_name="Previsão em minutos")

    def adicionar_acao(self, texto_acao, usuario):
        """
        Grava o conteudo e registra o usuário e data/hora.
        """
        data_hora = localtime(now()).strftime("%d/%m/%Y %H:%M:%S")
        nova_acao = f"\n\n[{data_hora} - {usuario.username}]:\n{texto_acao}"
        self.historico_acoes = (self.historico_acoes or "") + nova_acao
        self.save()        

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
            self.fechado_em = now()

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
