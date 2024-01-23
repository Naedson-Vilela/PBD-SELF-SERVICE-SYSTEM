from django.urls import path
from .views import (ProdutoApiView,
                    produto_list_create,
                    produto_detail,
                    mesa_list_create,
                    mesa_detail,
                    pedido_list_create,
                    pedido_detail,
                    produto_pedido_create,
                    )

urlpatterns = [
    path('produto/', produto_list_create, name='produto_api_view'),
    path('produto/<int:pk>/', produto_detail, name='produro_detail_api_view'),
    path('mesa/', mesa_list_create, name='mesa_api_view'),
    path('mesa/<int:pk>/', mesa_detail, name='mesa_detail_api_view'),
    path('pedido/', pedido_list_create, name='pedido_list_create'),
    path('pedido/<int:pk>/', pedido_detail, name='pedido_detail'),
    path('pedido/<int:pk>/adicionar-produto-pedido/', produto_pedido_create, name='create_produto_pedido'),
]
