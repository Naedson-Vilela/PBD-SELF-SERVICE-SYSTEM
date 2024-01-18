from django.urls import path
from .views import (ProdutoApiView,
                    produto_list_create,
                    produto_detail,
                    mesa_list_create,
                    mesa_detail,
                    )

urlpatterns = [
    path('produto/', produto_list_create, name='produto_api_view'),
    path('produto/<int:pk>/', produto_detail, name='produro_detail_api_view'),
    path('mesa/', mesa_list_create, name='mesa_api_view'),
    path('mesa/<int:pk>/', mesa_detail, name='mesa_detail_api_view'),
]