from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from utils import SerializerUtils
from .models import (Pedido,
                     ProdutoQuantidade,
                     Mesa,
                     Produto)
from .serializers import (PedidoSerializer,
                          ProdutoQuantidadeSerializer,
                          MesaSerializer,
                          ProdutoSerializer, ProdutoQuantidadeSerializerList, PedidoSerializerList,
                          ProdutoSerializerList)


@api_view(['GET', 'POST'])
def produto_list_create(request):

    if request.method == 'GET':
        produtos = Produto.objects.all()
        produtos_serializer = ProdutoSerializerList(produtos, many=True)

        return JsonResponse(produtos_serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.data
        produto_serializer = ProdutoSerializer(data=data)

        if produto_serializer.is_valid():
            produto_serializer.save()
            return JsonResponse(produto_serializer.data, status=201)
        return HttpResponse(produto_serializer.errors, status=400)


@api_view(['GET', 'DELETE', 'PUT'])
def produto_detail(request, pk):

    produto = get_object_or_404(Produto, pk=pk)

    try:
        produto = Produto.objects.get(pk=pk)
    except:
        return


    if request.method == 'GET':
        produto_serializer = ProdutoSerializerList(produto)
        return JsonResponse(produto_serializer.data)

    elif request.method == 'PUT':
        produto_novo = request.data
        produto_novo_serializer = ProdutoSerializer(produto, data=produto_novo)

        if produto_novo_serializer.is_valid():
            produto_novo_serializer.save()
            return JsonResponse(produto_novo_serializer.data, status=200)

    elif request.method == 'DELETE':
        produto.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def mesa_list_create(request):
    if request.method == 'GET':
        mesas = Mesa.objects.all()
        mesa_serializer = MesaSerializer(mesas, many=True)

        return JsonResponse(mesa_serializer.data, safe=False)

    if request.method == 'POST':
        data = request.data
        mesa_serializer = MesaSerializer(data=data)
        if mesa_serializer.is_valid():
            mesa_serializer.save()
            return JsonResponse(mesa_serializer.data, status=201)
        return HttpResponse(mesa_serializer.errors, status=400)


@api_view(['GET', 'DELETE', 'PUT'])
def mesa_detail(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)

    if request.method == 'GET':
        mesa_serializer = MesaSerializer(mesa)
        return JsonResponse(mesa_serializer.data)
    if request.method == 'PUT':
        mesa_nova = request.data
        mesa_nova_serializer = MesaSerializer(mesa, data=mesa_nova)
        if mesa_nova_serializer.is_valid():
            mesa_nova_serializer.save()
            return JsonResponse(mesa_nova_serializer.data, status=200)
    if request.method == 'DELETE':
        mesa.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def pedido_list_create(request):

    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        pedido_serializer = PedidoSerializerList(pedidos, many=True)
        return JsonResponse(pedido_serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.data
        pedido_serializer = PedidoSerializer(data=data)
        produtos_quantidades = data.get('produtos_quantidades')
        data.pop('produtos_quantidades')
        if pedido_serializer.is_valid():
            if all([ProdutoQuantidadeSerializer(data=item).is_valid(raise_exception=True) for item in produtos_quantidades]):
                pedido_serializer = pedido_serializer.criar_pedido_produtos_quantidades(data, produtos_quantidades)
                return JsonResponse(pedido_serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return HttpResponse(pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'GET':
        pedido_serializer = PedidoSerializerList(pedido, read_only=True)
        return JsonResponse(pedido_serializer.data, safe=False)

    elif request.method == 'PUT':
        try:
            pedido_novo = request.data.copy()
            pedido_novo.pop('produtos_quantidades')
            pedido_serializer = PedidoSerializer(pedido, pedido_novo, partial=True)
            if pedido_serializer.is_valid():
                if request.data.get('produtos_quantidades'):
                    produtos_quantidades = [ProdutoQuantidadeSerializer(data=item) for item in request.data['produtos_quantidades']]
                    flag = all([item.is_valid() for item in produtos_quantidades])
                    if flag:
                        for item in request.data['produtos_quantidades']:
                            produto_quantidade = get_object_or_404(ProdutoQuantidade, pk=item['id'])
                            produto_quantidade_serializer = ProdutoQuantidadeSerializer(produto_quantidade, item)
                            produto_quantidade_serializer.is_valid(raise_exception=True)
                            produto_quantidade_serializer.save()
                        pedido_serializer.save()
                        return JsonResponse(pedido_serializer.data, safe=False)
                    erros = SerializerUtils.combine_serializer_errors(produtos_quantidades)
                    return JsonResponse({'erros': erros}, status=status.HTTP_400_BAD_REQUEST)
                pedido_serializer.save()
                return JsonResponse(pedido_serializer.data, safe=False, status=status.HTTP_200_OK)
        except:
            return JsonResponse({'erro': 'JSON INVÁLIDO'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pedido.delete()
        return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def list_create_produto_quantidades(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'GET':
        produto_quantidades = ProdutoQuantidade.objects.filter(pedido=pedido)
        serializer = ProdutoQuantidadeSerializerList(produto_quantidades, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.data
        flag, serializer = ProdutoQuantidadeSerializer.create_produto_quantidade(pedido, data)
        if flag:
            return JsonResponse({'produto_quantidade': serializer}, safe=False, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def produto_quantidade_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'PUT':
        produto_quantidade = [ProdutoQuantidade.objects.get(pk=pk['id']) for pk in request.data]
        validate, serializer = ProdutoQuantidadeSerializer.update_many_produto_quantidade(produto_quantidade, request.data)
        if validate:
            return JsonResponse({'produto_quntidade': serializer}, safe=False, status=status.HTTP_200_OK)
        return JsonResponse(SerializerUtils.combine_serializer_errors(serializer.errors), safe=False, status=status)

    if request.method == 'DELETE':
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

