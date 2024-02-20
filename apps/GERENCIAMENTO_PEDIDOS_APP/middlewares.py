import requests
from django.conf import settings
from django.http import JsonResponse

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o cabeçalho Authorization está presente na solicitação
        if 'Authorization' in request.headers:
            # Obtém o token JWT do cabeçalho Authorization
            token = request.headers['Authorization'].split(' ')[1]
            # Faz uma solicitação para o microserviço de autenticação para validar o token JWT
            response = requests.post(
                f'{settings.AUTH_MICROSERVICE_URL}/validate/',
                headers={'Authorization': f'Bearer {token}'}
            )
            print(response)

            if response.status_code == 200:
                # Token é válido, permita que a solicitação continue
                return self.get_response(request)
            else:
                # Token é inválido, retorne uma resposta de erro de autenticação
                return JsonResponse({'error': 'Token de autenticação inválido'}, status=401)
        else:
            # Cabeçalho Authorization não está presente na solicitação, retorne uma resposta de erro de autenticação
            return JsonResponse({'error': 'Cabeçalho de autorização ausente'}, status=401)
