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
        ('Grupo A','Grupo A'),
        ('Grupo B', 'Grupo B'),
    ]
    RECURSO_CRITICIDADE_MAP = {
        'Alfa':'Baixa',
        'Beta':'Baixa',
        'Gama':'Baixa',

        'Delta':'Média',
        'Epsilon':'Média',
        'Zeta':'Média',

        'Eta':'Baixa',
        'Teta':'Baixa',
        'Iota':'Baixa',
    }
    RECURSO_RESPONSAVEL_MAP = {
        'Alfa':'Armando Pinto',
        'Beta':'Dolores Fuertes',
        'Gama':'Tomás Turbando',

        'Delta':'Elvira Alface',
        'Epsilon':'Noé Pego',
        'Zeta':'Paulo Cintura',

        'Eta':'Alceu Melancia',
        'Teta':'Rosa Chiclete',
        'Iota':'Tobias Moco',
    }
    RECURSOS_CHOICES = [
        ('Alfa','Alfa'),
        ('Beta','Beta'),
        ('Gama','Gama'),
        ('Delta','Delta'),
        ('Epsilon','Epsilon'),
        ('Zeta','Zeta'),
        ('Eta','Eta'),
        ('Teta','Teta'),
        ('Iota','Iota'),
    ]

    # Identificadores do Incidente
    codigo_incidente = models.CharField(max_length=50, verbose_name="Incidente", unique=True)
    codigo_sx = models.CharField(max_length=50, verbose_name="Código Crítico", default="", blank=True)
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
