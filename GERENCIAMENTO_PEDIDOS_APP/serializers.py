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

    @staticmethod
    def combine_serializer_errors(list_serializers):
        combined_errors = []
        for serializer in list_serializers:
            serializer.is_valid()
            if serializer.errors:
                combined_errors.append(serializer.errors)
        return combined_errors


class PedidoSerializer(serializers.ModelSerializer):

    produtos_quantidades = ProdutoQuantidadeSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    @staticmethod
    def criar_pedido_produtos_quantidades(pedido, produto_quantidade):
        pedido['mesa_id'] = Mesa.objects.get(pk=pedido.get('mesa_id'))
        pedido_object = Pedido.objects.create(**pedido)
        for item in produto_quantidade:
            item['produto_id'] = Produto.objects.get(pk=item.get('produto_id'))
        pedidos_quantides = [ProdutoQuantidade.objects.create(**item) for item in produto_quantidade]
        pedido_object.produtos_quantidades.set(pedidos_quantides)
        return PedidoSerializer(pedido, read_only=True)
