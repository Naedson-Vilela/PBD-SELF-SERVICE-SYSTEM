from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

class ProdutoApiView(generics.ListCreateAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# @api_view(['POST'])
# def ProdutoApiViewDjango(request):
#
#     object = request.data
#
#     Produto.objects.create(nome_produto=object.get('nome_produto'),
#                            categoria_id=Categoria.objects.get(id=object.get('categoria_id')),
#                            preco=object.get('preco'),
#                            descricao=object.get('descricao'),
#                            is_cozinha=object.get('is_cozinha')
#                            )
#
#     return HttpResponse(request.data)

@api_view(['GET', 'POST'])
def produto_list_create(request):

    if request.method == 'GET':
        produtos = Produto.objects.all()
        produtos_serializer = ProdutoSerializer(produtos, many=True)

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



    if request.method == 'GET':
        produto_serializer = ProdutoSerializer(produto)
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






