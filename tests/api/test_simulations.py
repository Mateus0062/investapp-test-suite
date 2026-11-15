"""Testes de simulations.

Responsavel: Integrantes 5 e 6 - POST /api/simulate/yield-monthly e /api/simulate/tax-withdrawal.
"""

import pytest
import requests


# Integrante 5 - Gustavo Morais - POST /api/simulate/yield-monthly

@pytest.mark.parametrize("months", [6, 12, 24])
def test_simulate_yield_monthly(base_url, auth_headers, months):
    """
    Testa a simulação de rendimento mensal (POST /api/simulate/yield-monthly) para diferentes períodos.
    Valida status 200, chaves de resumo do portfólio e detalhamento mês a mês.
    """
    payload = {"months": months}

    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json=payload,
        headers=auth_headers,
    )

    assert response.status_code == 200, (
        f"Esperado status 200, obtido {response.status_code}. Resposta: {response.text}"
    )

    data = response.json()
    assert isinstance(data, dict), "O retorno da simulação de rendimento mensal deve ser um objeto JSON"

    expected_keys = {
        "monthly_breakdown",
        "type_summary",
        "total_portfolio_invested",
        "total_portfolio_future",
        "total_portfolio_profit",
        "total_portfolio_growth_pct",
    }
    assert expected_keys <= set(data.keys()), f"Chaves ausentes no retorno: {expected_keys - set(data.keys())}"

    breakdown = data["monthly_breakdown"]
    assert isinstance(breakdown, list), "monthly_breakdown deve ser uma lista"
    assert len(breakdown) == months, f"Esperado {months} meses no breakdown, obtido {len(breakdown)}"

    for idx, mes_info in enumerate(breakdown, start=1):
        assert mes_info["month"] == idx
        assert isinstance(mes_info["assets"], list)
        assert isinstance(mes_info["total_month_value"], (int, float))


def test_simulate_yield_monthly_default_months(base_url, auth_headers):
    """
    Testa a simulação de rendimento mensal omitindo 'months' (valor padrão de 12 meses no Swagger).
    """
    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json={},
        headers=auth_headers,
    )

    assert response.status_code == 200, (
        f"Esperado status 200, obtido {response.status_code}. Resposta: {response.text}"
    )
    data = response.json()
    assert isinstance(data, dict)
    assert len(data["monthly_breakdown"]) == 12


def test_simulate_yield_monthly_sem_token(base_url):
    """
    Valida que a simulação de rendimento mensal exige autenticação (HTTP 401 sem token).
    """
    response = requests.post(
        f"{base_url}/api/simulate/yield-monthly",
        json={"months": 12},
    )

    assert response.status_code == 401
    assert response.json().get("detail") == "Not authenticated"


# Integrante 6 - Júlia Suriani - GET/DELETE /api/investments POST /api/simulate/tax-withdrawal
def test_simulate_tax_withdrawal(base_url, auth_headers):
    """
    Testa a simulação de resgate com otimização fiscal (POST /api/simulate/tax-withdrawal).
    Valida se a API retorna status 200 e a lista estruturada com os cálculos fiscais.
    """
    payload = {
        "target_amount": 1000.00
    }

    response = requests.post(f"{base_url}/api/simulate/tax-withdrawal", json=payload, headers=auth_headers)

    assert response.status_code == 200, f"Esperado status 200, obtido {response.status_code}. Resposta: {response.text}"

    data = response.json()
    assert isinstance(data, list), "O retorno da simulação fiscal deve ser uma lista JSON"

    expected_keys = {
        "asset_name",
        "asset_type",
        "current_val",
        "tax_due",
        "effective_tax_rate",
        "net_amount",
        "is_exempt",
    }
    for item in data:
        assert expected_keys <= set(item.keys()), f"Chaves ausentes no item fiscal: {expected_keys - set(item.keys())}"
        assert isinstance(item["tax_due"], (int, float))
        assert isinstance(item["net_amount"], (int, float))
        assert isinstance(item["is_exempt"], bool)
