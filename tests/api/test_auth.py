import os
import requests

TEST_USER = os.getenv("TEST_USER")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def test_login_sucesso(base_url):
    """Valida o login com credenciais corretas e o retorno do token JWT."""
    print(f"\n[TEST_AUTH] Testando endpoint /api/login para o usuário: '{TEST_USER}'")

    payload = {"username": TEST_USER, "password": TEST_PASSWORD}
    response = requests.post(f"{base_url}/api/login", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_credenciais_invalidas(base_url):
    """Valida a recusa de autenticação para senhas incorretas (HTTP 400)."""
    payload = {"username": TEST_USER, "password": "senha_invalida_xyz"}
    response = requests.post(f"{base_url}/api/login", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Usuário ou senha incorretos"


# ---------------------------------------------------------------------------
# Cenários adicionais do Líder (além dos fornecidos no roteiro)
# ---------------------------------------------------------------------------

def test_login_usuario_inexistente(base_url):
    """Valida que um usuário que não existe recebe a mesma recusa (HTTP 400),
    sem revelar se o problema foi o usuário ou a senha."""
    payload = {"username": "usuario_inexistente_investapp_zz", "password": "qualquer"}
    response = requests.post(f"{base_url}/api/login", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Usuário ou senha incorretos"


def test_token_permite_acesso_a_rota_protegida(base_url, auth_headers):
    """Valida que o token obtido pela fixture de sessão é aceito em uma rota protegida."""
    response = requests.get(f"{base_url}/api/investments", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
