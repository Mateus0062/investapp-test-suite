"""Teste de carga leve da API InvestApp (extra - seção 9 do roteiro: k6 / Locust).

Contribuição: Luiz Felipe Silva Araujo.
Usa apenas o endpoint público GET /api/assets e uma carga baixa,
para não sobrecarregar o ambiente compartilhado pelo grupo
"""
from locust import HttpUser, between, task


class UsuarioConsultaAtivos(HttpUser):
    """Simula um usuário consultando a tabela pública de ativos."""

    wait_time = between(1, 3)

    @task
    def listar_ativos(self):
        with self.client.get("/api/assets", name="GET /api/assets", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status inesperado: {response.status_code}")
            elif not isinstance(response.json(), list) or not response.json():
                response.failure("Lista de ativos vazia ou inválida")
            else:
                response.success()
