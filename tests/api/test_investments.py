"""Testes de investments.

Responsavel: Integrantes 3, 4 e 7 - POST/GET/DELETE /api/investments e DDT via CSV.
"""

# Integrante 4 - Júlia Suriani - GET/DELETE /api/investments
import pytest
import requests


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


# Integrante 7 - Júlia Suriani - 	DDT via CSV
import csv
import os
import pytest
import requests

def carregar_dados_csv():
    """Lê os dados do CSV de investimentos para testes parametrizados (DDT)."""
    caminho_csv = os.path.join(os.path.dirname(__file__), "..", "data", "dados_investimentos.csv")
    dados = []
    if os.path.exists(caminho_csv):
        with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                dados.append((
                    linha["asset_name"],
                    float(linha["amount"]),
                    float(linha["purchase_price"]),
                    int(linha["days_invested"]),
                    int(linha["planned_days"]),
                    int(linha["status_esperado"])
                ))
    return dados

@pytest.mark.parametrize("asset_name, amount, purchase_price, days_invested, planned_days, status_esperado", carregar_dados_csv())
def test_create_investment_ddt(base_url, auth_headers, asset_name, amount, purchase_price, days_invested, planned_days, status_esperado):
    """
    Teste Orientado a Dados (DDT) para criação de investimentos via CSV.
    Responsável: Integrante 7.
    """
    payload = {
        "asset_name": asset_name,
        "amount": amount,
        "purchase_price": purchase_price,
        "days_invested": days_invested,
        "planned_days": planned_days
    }

    response = requests.post(f"{base_url}/api/investments", json=payload, headers=auth_headers)
    assert response.status_code == status_esperado, f"Esperado status {status_esperado}, obtido {response.status_code}. Resposta: {response.text}"
