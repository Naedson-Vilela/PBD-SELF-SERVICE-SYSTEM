from django.db import models
from django.utils.translation import gettext_lazy as _


class Mesa(models.Model):

    class StatusMesaChoice(models.TextChoices):
        OCUPADA = 'OCUPADA', _('Ocupada')
        LIVRE = 'LIVRE', _('Livre')
    
    status = models.CharField(max_length=7,
                              blank=False, 
                              choices=StatusMesaChoice.choices,
                              default=StatusMesaChoice.LIVRE
                              )
    numero_mesa = models.IntegerField(unique=True)

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero_mesa']

    def __str__(self):
        return f'{self.numero_mesa}'


class Categoria(models.Model):

    nome_categoria = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return f'{self.nome_categoria}'

class Produto(models.Model):

    imagem = models.ImageField(blank=True)
    nome_produto = models.CharField(max_length=100)
    categoria_id = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.SET_NULL, null=True)
    preco = models.FloatField()
    descricao = models.TextField(blank=True)
    is_cozinha = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['id']

    def __str__(self):
        return f'{self.nome_produto}'


class ProdutoQuantidade(models.Model):

    produto_id = models.ForeignKey(Produto, related_name='produtos_pedidos', on_delete=models.DO_NOTHING)
    quantidade_produtos = models.IntegerField(blank=False, null=False)

    class Meta:
        verbose_name = 'Produto pedido'
        verbose_name_plural = 'Produtos pedidos'
        ordering = ['id']

    def __str__(self):
        return f'{self.id}'

class Pedido(models.Model):
    class StatusPedidoChoice(models.TextChoices):
        REALIZADO = 'REALIZADO', _('Realizado')
        EM_EMPRODUCAO = 'PRODUCAO', _('Em produção')
        PRONTO_SERVIR = 'PRONTO', _('Pronto para servir')
        ENTREGUE = 'ENTREGUE', _('Entregue')
        FINALIZADO = 'FINALIZADO', _('Finalizado')
        CANCELADO = 'CANCELADO', _('Cancelado')
        RECUSADO = 'RECUSADO', _('Recusado')
        PROBLEMA_PEDIDO = 'PROBLEMA_PEDIDO', _('Problema com pedido')

    produtos_quantidades = models.ManyToManyField(ProdutoQuantidade, blank=True)
    mesa_id = models.ForeignKey(Mesa, related_name='pedidos', on_delete=models.DO_NOTHING)
    nome_cliente = models.CharField(max_length=50, blank=False)
    data_hora = models.DateTimeField(auto_now=True)
    status_pedido = models.CharField(max_length=15,
                                     choices=StatusPedidoChoice.choices,
                                     default=StatusPedidoChoice.REALIZADO)



    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']

    def __str__(self):
        return f'{self.id}'




