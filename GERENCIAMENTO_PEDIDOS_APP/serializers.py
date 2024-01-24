from rest_framework import serializers
from .models import *

class MesaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mesa
        fields = (
            '__all__'
        )


class CategoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produto
        fields = '__all__'


class ProdutoQuantidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProdutoQuantidade
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):

    produtos_quantidades = ProdutoQuantidadeSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'
