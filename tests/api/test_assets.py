"""Testes de ativos (Integrante 2).

Rotas cobertas (conferidas no Swagger):
- GET /api/assets  -> lista de ativos com taxa anual
- PUT /api/assets  -> atualiza a taxa anual de um ativo (body: asset_name, annual_rate)
"""
import os
import random

import pytest
import requests

TEST_USER = os.getenv("TEST_USER", "grupo")

# Ativo exclusivo do grupo para o teste de atualização.
# Usamos um nome próprio em vez de "CDB" ou "Poupança" para não alterar
# as taxas que as outras turmas usam nas simulações (o ambiente é compartilhado).
ATIVO_DO_GRUPO = f"QA Taxa {TEST_USER}"


def buscar_ativos(base_url, headers=None):
    """Faz GET /api/assets e devolve a lista já validada como 200."""
    response = requests.get(f"{base_url}/api/assets", headers=headers)
    assert response.status_code == 200, f"GET /api/assets falhou: {response.text}"
    return response.json()


# ---------------------------------------------------------------------------
# GET /api/assets
# ---------------------------------------------------------------------------

def test_listar_ativos_publicos(base_url):
    """Valida a consulta à tabela pública de taxas de ativos sem autenticação."""
    response = requests.get(f"{base_url}/api/assets")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_estrutura_dos_ativos(base_url):
    """Valida que cada ativo segue o schema AssetRateSchema do Swagger."""
    ativos = buscar_ativos(base_url)

    for ativo in ativos:
        assert set(ativo.keys()) >= {"asset_name", "asset_type", "annual_rate"}
        assert isinstance(ativo["asset_name"], str) and ativo["asset_name"]
        assert isinstance(ativo["asset_type"], str) and ativo["asset_type"]
        assert isinstance(ativo["annual_rate"], (int, float))


@pytest.mark.parametrize("nome_ativo", ["Poupança", "CDB"])
def test_ativos_basicos_disponiveis(base_url, nome_ativo):
    """Valida que os ativos usados nos testes de investimento existem na tabela."""
    nomes = {ativo["asset_name"] for ativo in buscar_ativos(base_url)}

    assert nome_ativo in nomes


def test_listar_ativos_autenticado(base_url, auth_headers):
    """Valida que a listagem também funciona com o token (a rota declara segurança no Swagger)."""
    ativos = buscar_ativos(base_url, headers=auth_headers)

    assert isinstance(ativos, list)
    assert len(ativos) > 0


# ---------------------------------------------------------------------------
# PUT /api/assets
# ---------------------------------------------------------------------------

def test_atualizar_taxa_ativo(base_url, auth_headers):
    """Atualiza a taxa do ativo do grupo e confirma o novo valor via GET."""
    # Garante que o ativo do grupo existe antes de atualizar
    setup = requests.put(
        f"{base_url}/api/assets",
        json={"asset_name": ATIVO_DO_GRUPO, "annual_rate": 5.0},
        headers=auth_headers,
    )
    assert setup.status_code == 200, f"Falha ao preparar o ativo: {setup.text}"

    # Taxa aleatória: garante que o teste prova uma mudança real a cada execução
    nova_taxa = round(random.uniform(6.0, 20.0), 2)
    response = requests.put(
        f"{base_url}/api/assets",
        json={"asset_name": ATIVO_DO_GRUPO, "annual_rate": nova_taxa},
        headers=auth_headers,
    )
    print(f"\n[TEST_ASSETS] PUT '{ATIVO_DO_GRUPO}' -> {nova_taxa}% | resposta: {response.text}")

    assert response.status_code == 200

    taxas_do_ativo = [
        a["annual_rate"]
        for a in buscar_ativos(base_url, headers=auth_headers)
        if a["asset_name"] == ATIVO_DO_GRUPO
    ]
    assert taxas_do_ativo, f"Ativo '{ATIVO_DO_GRUPO}' não apareceu na listagem após o PUT"
    assert nova_taxa in [pytest.approx(t) for t in taxas_do_ativo]


def test_atualizar_taxa_sem_token(base_url):
    """Valida que a atualização de taxa é bloqueada sem autenticação (HTTP 401)."""
    response = requests.put(
        f"{base_url}/api/assets",
        json={"asset_name": ATIVO_DO_GRUPO, "annual_rate": 1.0},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"