from django.urls import path
from .views import (ProdutoApiView,
                    produto_list_create,
                    produto_detail)

urlpatterns = [
    path('produto/', produto_list_create, name='produto_api_view'),
    path('produto/<int:pk>/', produto_detail, name='produro_detail_api_view')
]