from django.test import TestCase

# Create your tests here.

dicionario = {
    "mesa_id": 1,
    "nome_cliente": "NETO",
    "status_pedido": "REALIZADO",
    "pedido_produto": [
        {
            "produto_id": 10,
            "quantidade_produtos": 2
        },
        {
            "produto_id": 10,
            "quantidade_produtos": 2
        },
        {
            "produto_id": 10,
            "quantidade_produtos": 2
        }
    ]
}

dicionario.pop('pedido_produto')
print(dicionario)



