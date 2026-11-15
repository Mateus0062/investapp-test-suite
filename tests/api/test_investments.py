"""Testes de investments.

Responsavel: Integrantes 3, 4 e 7 - POST/GET/DELETE /api/investments e DDT via CSV.
"""

import pytest
import requests


# Integrante 3 - Luca Barbosa Rodrigues - POST /api/investments
def test_criar_investimento_poupanca_valido(base_url, auth_headers):
    """Valida a criação de um investimento válido em Poupança (HTTP 201)."""
    payload = {
        "asset_name": "Poupança",
        "amount": 1000.00,
        "purchase_price": 1.00,
        "days_invested": 30,
        "planned_days": 365,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["asset_name"] == payload["asset_name"]
    assert data["amount"] == payload["amount"]


def test_criar_investimento_cdb_valido(base_url, auth_headers):
    """Valida a criação de um investimento válido em CDB (HTTP 201)."""
    payload = {
        "asset_name": "CDB",
        "amount": 5000.00,
        "purchase_price": 1.00,
        "days_invested": 180,
        "planned_days": 720,
    }

    response = requests.post(
        f"{base_url}/api/investments",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["asset_name"] == payload["asset_name"]
    assert data["amount"] == payload["amount"]


# Integrante 4 - Júlia Suriani - GET/DELETE /api/investments
def test_list_investments(base_url, auth_headers):
    """
    Testa a listagem de investimentos (GET /api/investments).
    Valida se a rota retorna status 200 e uma lista estruturada.
    """
    response = requests.get(f"{base_url}/api/investments", headers=auth_headers)

    assert response.status_code == 200, f"Esperado status 200, obtido {response.status_code}"
    data = response.json()
    assert isinstance(data, list), "O retorno da API deve ser uma lista de investimentos"


def test_delete_investment(base_url, auth_headers):
    """
    Testa a exclusão de um investimento (DELETE /api/investments/{id}).
    """
    # 1. Fazemos um GET primeiro para descobrir se existe algum investimento cadastrado
    list_response = requests.get(f"{base_url}/api/investments", headers=auth_headers)
    assert list_response.status_code == 200, "Erro ao listar investimentos para preparar o teste de exclusão."

    investments = list_response.json()

    if len(investments) > 0:
        # Se já houver investimentos, pegamos o ID do primeiro da lista para excluir
        investment_id = investments[0].get("id") or investments[0].get("_id")

        response = requests.delete(f"{base_url}/api/investments/{investment_id}", headers=auth_headers)

        # Valida se a exclusão retornou sucesso (200 OK ou 204 No Content)
        assert response.status_code in [200, 204], f"Erro ao excluir investimento. Status recebido: {response.status_code}"
    else:
        # Caso a base de testes esteja vazia, podemos simular a tentativa de deletar um ID fictício
        # ou validar que o endpoint lida corretamente com IDs inexistentes (ex: 99999 -> 404 ou 400)
        investment_id = 99999
        response = requests.delete(f"{base_url}/api/investments/{investment_id}", headers=auth_headers)

        # Dependendo da regra da API, deletar algo inexistente pode retornar 404
        assert response.status_code in [404, 400], f"Esperado status de erro para ID inexistente, recebido: {response.status_code}"