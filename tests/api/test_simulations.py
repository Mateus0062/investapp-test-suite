"""Testes de simulations.

Responsavel: Integrantes 5 e 6 - POST /api/simulate/yield-monthly e /api/simulate/tax-withdrawal.
"""
# Integrante 6 - Júlia Suriani - GET/DELETE /api/investments POST /api/simulate/tax-withdrawal

import pytest
import requests

def test_simulate_tax_withdrawal(base_url, auth_headers):
    """
    Testa a simulação de resgate com otimização fiscal (POST /api/simulate/tax-withdrawal).
    Valida se a API retorna status 200 e a estrutura esperada com os cálculos fiscais.
    """
    payload = {
        "investment_id": 1,
        "withdrawal_amount": 1500.00,
        "target_amount": 1000.00
    }
    
    response = requests.post(f"{base_url}/api/simulate/tax-withdrawal", json=payload, headers=auth_headers)
    
    assert response.status_code == 200, f"Esperado status 200, obtido {response.status_code}. Resposta: {response.text}"
    
    data = response.json()
    assert isinstance(data, dict), "O retorno da simulação fiscal deve ser um objeto JSON"