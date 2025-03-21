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

    CRITICIDADE_CHOICES = [
        ('Crítico','Crítico'),
        ('Muito Crítico','Muito Crítico'),
        ('Hiper Crítico','Hiper Crítico'),
    ]

    # Identificadores
    codigo_incidente = models.CharField(max_length=50, verbose_name="Incidente")
    codigo_sx = models.CharField(max_length=50, verbose_name="SX", default="", blank=True)
    recurso = models.CharField(max_length=50, verbose_name="Recurso")
    responsavel = models.CharField(max_length=200, verbose_name="Responsável")

    # Caixas de Texto
    problema_apresentado = models.TextField(verbose_name="Problema Apresentado")
    acoes = models.TextField(verbose_name="Ações")
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
        choices=CRITICIDADE_CHOICES, 
        default='Crítico', 
        verbose_name="Criticidade"
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

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_incidente} - {self.responsavel}"

    def __str__(self):
        return f"{self.codigo_incidente} - {self.responsavel}"

    def __str__(self):
        return f"{self.codigo_incidente} - {self.responsavel}"

class TicketImage(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tickets/images/')

    def __str__(self):
        return f"Imagem do Ticket {self.ticket.codigo_incidente}"

#! Campo de `Upload de Arquivos` desativado
# class TicketFile(models.Model):
#     ticket = models.ForeignKey(Ticket, related_name='files', on_delete=models.CASCADE)
#     file = models.FileField(upload_to='tickets/files/')

#     def __str__(self):
#         return f"Arquivos do Ticket {self.ticket.codigo_incidente}"