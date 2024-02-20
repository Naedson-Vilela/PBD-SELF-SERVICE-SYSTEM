# Generated by Django 5.0.1 on 2024-02-20 04:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_categoria', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('OCUPADA', 'Ocupada'), ('LIVRE', 'Livre')], default='LIVRE', max_length=7)),
                ('numero_mesa', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Mesa',
                'verbose_name_plural': 'Mesas',
                'ordering': ['numero_mesa'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, upload_to='')),
                ('nome_produto', models.CharField(max_length=100)),
                ('preco', models.FloatField()),
                ('descricao', models.TextField(blank=True)),
                ('is_cozinha', models.BooleanField(default=False)),
                ('categoria_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produtos', to='GERENCIAMENTO_PEDIDOS_APP.categoria')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ProdutoQuantidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_produtos', models.IntegerField()),
                ('produto_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='produtos_pedidos', to='GERENCIAMENTO_PEDIDOS_APP.produto')),
            ],
            options={
                'verbose_name': 'Produto pedido',
                'verbose_name_plural': 'Produtos pedidos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cliente', models.CharField(max_length=50)),
                ('data_hora', models.DateTimeField(auto_now=True)),
                ('status_pedido', models.CharField(choices=[('REALIZADO', 'Realizado'), ('PRODUCAO', 'Em produção'), ('PRONTO', 'Pronto para servir'), ('ENTREGUE', 'Entregue'), ('FINALIZADO', 'Finalizado'), ('CANCELADO', 'Cancelado'), ('RECUSADO', 'Recusado'), ('PROBLEMA_PEDIDO', 'Problema com pedido')], default='REALIZADO', max_length=15)),
                ('mesa_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pedidos', to='GERENCIAMENTO_PEDIDOS_APP.mesa')),
                ('produtos_quantidades', models.ManyToManyField(blank=True, to='GERENCIAMENTO_PEDIDOS_APP.produtoquantidade')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['id'],
            },
        ),
    ]
