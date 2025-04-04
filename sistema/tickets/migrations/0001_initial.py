# Generated by Django 5.1.7 on 2025-03-25 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_incidente', models.CharField(max_length=50, verbose_name='Incidente')),
                ('codigo_sx', models.CharField(blank=True, default='', max_length=50, verbose_name='SX')),
                ('recurso', models.CharField(choices=[('Balcão Único', 'Balcão Único'), ('Central de Transplantes', 'Central de Transplantes'), ('CNH', 'CNH'), ('CRV', 'CRV'), ('Plataforma REDE SP.GOV.BR', 'Plataforma REDE SP.GOV.BR'), ('Portal Detran', 'Portal Detran'), ('Portal Poupatempo', 'Portal Poupatempo'), ('Prova Eletrônica', 'Prova Eletrônica'), ('SEI', 'SEI'), ('TOTEM', 'TOTEM'), ('Agendamento Universal - Agenda SP', 'Agendamento Universal - Agenda SP'), ('CAR - Cadastro de Atendimento e Relacionamento', 'CAR - Cadastro de Atendimento e Relacionamento'), ('Delegacia Eletrônica', 'Delegacia Eletrônica'), ('e-Vistoria', 'e-Vistoria'), ('Multas DER', 'Multas DER'), ('Poupafila Centralizado', 'Poupafila Centralizado'), ('SIM', 'SIM'), ('SPJ', 'SPJ'), ('Aplicações Mobile', 'Aplicações Mobile'), ('Detecta', 'Detecta'), ('Inquérito Eletrônico', 'Inquérito Eletrônico'), ('Ipva Online', 'Ipva Online'), ('Rede Palácio do Governo', 'Rede Palácio do Governo'), ('S4SP', 'S4SP'), ('Sistema Alpha', 'Sistema Alpha'), ('Valid - IIRGD', 'Valid - IIRGD')], max_length=50, verbose_name='Recurso')),
                ('problema_apresentado', models.CharField(max_length=50, verbose_name='Problema Apresentado')),
                ('historico_acoes', models.TextField(blank=True, editable=False, verbose_name='Histórico de Ações')),
                ('solucao_contorno', models.TextField(blank=True, default='', null=True, verbose_name='Solução de Contorno')),
                ('link_alerta', models.URLField(blank=True, null=True, verbose_name='Alerta Dynatrace')),
                ('link_itsm', models.URLField(blank=True, null=True, verbose_name='Link do Incidente ITSM')),
                ('grupo_suporte', models.CharField(choices=[('COI - Grupo de Operações Integradas', 'COI - Grupo de Operações Integradas'), ('COI - Gestão de Problemas', 'COI - Gestão de Problemas'), ('Operações IBM', 'Operações IBM')], default='', max_length=100, verbose_name='Grupo de Suporte')),
                ('responsavel', models.CharField(editable=False, max_length=100, verbose_name='Responsável')),
                ('analista', models.CharField(choices=[('Leandro Fratel', 'Leandro Fratel'), ('Heráclito Teixeira', 'Heráclito Teixeira'), ('Camilla Gama', 'Camilla Gama')], default='Não Atribuido', max_length=100, verbose_name='Analista')),
                ('status', models.CharField(choices=[('Aberto', 'Aberto'), ('Fechado', 'Fechado'), ('Resolvido', 'Resolvido'), ('Em Andamento', 'Em Andamento'), ('Designado', 'Designado'), ('Em Análise', 'Em Análise'), ('Sala de Crise', 'Sala de Crise')], default='Aberto', max_length=50, verbose_name='Status')),
                ('criticidade', models.CharField(choices='', default='Crítico', editable=False, max_length=50, verbose_name='Criticidade')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('fechado_em', models.DateTimeField(blank=True, null=True)),
                ('previsao', models.IntegerField(blank=True, null=True, verbose_name='Previsão em minutos')),
            ],
        ),
        migrations.CreateModel(
            name='TicketImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tickets/images/')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tickets.ticket')),
            ],
        ),
    ]
