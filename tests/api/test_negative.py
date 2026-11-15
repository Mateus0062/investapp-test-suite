"""Testes de cenários negativos e validação de erros da API.

Responsável: Integrante 8.
"""

# Integrante 8 - Júlia Suriani - Testes de cenários negativos e validação de erros da API
import pytest
import requests


def test_unauthorized_access(base_url):
    """
    Valida que acessar uma rota protegida sem token JWT retorna erro de autorização (401).
    """
    response = requests.get(f"{base_url}/api/investments")
    assert response.status_code == 401, f"Esperado status 401 para acesso sem token, obtido {response.status_code}"


def test_create_investment_invalid_payload(base_url, auth_headers):
    """
    Valida que enviar um payload incompleto ou inválido na criação de investimentos retorna erro (422).
    """
    # Payload faltando campos obrigatórios
    payload_invalido = {
        "asset_name": ""
    }
    
    response = requests.post(f"{base_url}/api/investments", json=payload_invalido, headers=auth_headers)
    assert response.status_code == 422, f"Esperado status 422 para payload inválido, obtido {response.status_code}"


def test_delete_investment_nonexistent(base_url, auth_headers):
    """
    Valida a tentativa de excluir um ID de investimento que não existe no sistema (404 ou 400).
    """
    fake_id = 999999
    response = requests.delete(f"{base_url}/api/investments/{fake_id}", headers=auth_headers)
    assert response.status_code in [404, 400], f"Esperado erro para ID inexistente, obtido {response.status_code}"