# investapp-test-suite

Suíte de testes automatizados de API REST (Pytest + Requests) do **InvestApp**.
Repositório *test-only*: os testes chamam diretamente a API publicada no AWS API Gateway.

- Swagger: https://5bm1nctd1f.execute-api.us-east-1.amazonaws.com/docs

## Setup (cada integrante)

```bash
# Codespace
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# ou Local (Anaconda, Python 3.11)
conda create -n investapp-tests python=3.11 -y
conda activate investapp-tests
pip install -r requirements.txt
```

O `.env` **não** está no repositório (tem a senha). Crie o seu a partir do modelo:

```bash
cp .env.example .env   # depois edite TEST_USER e TEST_PASSWORD
```

O `.vscode/launch.json` também não é versionado (ele tem credenciais). Peça ao Líder o arquivo
ou copie o modelo do roteiro (seção 3).

## Execução

```bash
python -m pytest tests/api -v -s
python -m pytest tests/api --cov=tests/api --cov-report=term-missing
```

Também roda pelo painel Testing (Tubo de Ensaio) do VS Code e com F5 em "Debug: Pytest API Tests".

## Fixtures disponíveis (`tests/api/conftest.py`)

| Fixture        | Escopo  | O que entrega                                      |
|----------------|---------|----------------------------------------------------|
| `base_url`     | session | URL base da API                                    |
| `auth_token`   | session | Token JWT do usuário do `.env` (login feito 1 vez) |
| `auth_headers` | session | `{"Authorization": "Bearer <token>"}`              |

Para usar, basta pedir pelo nome no parâmetro do teste, sem importar nada:

```python
def test_exemplo(base_url, auth_headers):
    r = requests.get(f"{base_url}/api/investments", headers=auth_headers)
    assert r.status_code == 200
```

## Divisão de tarefas

| Integrante    | Arquivo(s)                                   | Escopo |
|---------------|----------------------------------------------|--------|
| 1 (Líder)     | configs, `conftest.py`, `test_auth.py`       | Setup e autenticação |
| 2             | `test_assets.py`                             | GET /api/assets, atualização de taxa |
| 3             | `test_investments.py`                        | POST /api/investments (válidos) |
| 4             | `test_investments.py`                        | GET /api/investments, DELETE /api/investments/{id} |
| 5             | `test_simulations.py`                        | Simulação de rendimento mensal |
| 6             | `test_simulations.py`                        | Simulação de resgate com otimização fiscal |
| 7             | `test_investments.py` + `tests/data/dados_investimentos.csv` | DDT via CSV |
| 8             | (a definir)                                  | Cenários negativos (400, 401, 422) |

> **Atenção às rotas reais (conferidas no Swagger):** algumas diferem do texto do roteiro.
> - Atualizar taxa: `PUT /api/assets` (não existe `/api/assets/{asset_id}/rate`)
> - Simulações: `/api/simulate/yield-monthly` e `/api/simulate/tax-withdrawal` (não `/api/simulations/...`)
>
> Confiram o corpo esperado de cada rota no Swagger antes de escrever os testes.

Cada integrante deve fazer **os próprios commits** nos seus arquivos, porque o professor verifica o histórico.
