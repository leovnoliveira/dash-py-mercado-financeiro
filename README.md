# Dashbaord de acompanhamento do Mercado Financeiro

Dashboard para acompanhamento de ativos de mercado financeiro em tempo real. 

Projeto final de curso, totalmente versionado em python.


Este dashboard está dividido em:


A) Índices de mercado em tempo real
B) Gráfico de cotações em tempo real
C) Indicadores econômicos
D) Estatísticas
E) Notícias

## Python Version

Python 3.13.1 (Dec. 3, 2024)

## Versionamento

Utilizou-se o pacote `pyenv` para gerenciar e instalar versões do python na minha máquina, a qual pode ser consultada em [python-version](./.python-version).

## Dependência de Pacotes

Realizada via biblioteca `poetry`, instalar por `pipx` (add global para todos os usuários da minha máquina) e adicionada para meu path de variáveis para gerenciamento fácil de ambiente virtual.

### Step by step: 

No termina do GitBash, faça:

1. `pip install pipx` para instalar o `pipx` (usuário)
2. `pipx install poetry` para instalar o `poetry` à sua máquina.
3. poetry init (para criar o arquivo pyproject.toml)
4. Ou, melhor ainda, faça `poetry new nome-do-projeto`, que já cria uma ambiente básico de projeto, com pasta de test, pasta src, o arquivo `pyproject.toml` e um `README.md`.
5. `poetry add selenium` para adicionar o pacote `selenium` ao `pyproject.toml`.
6. `poetry run activate` para ativar seu ambiente virtual com o pacote `selenium`. Este passo irá adicionar uma pasta .venv no diretório do seu projeto.
7. `poetry run python -m modulo-python` para rodar seu módulo python ou `poetry run python archive.py` para rodar scripts python isoladamente. 

* Para mais detalhes, clique em [pipx](https://python.land/virtual-environments/pipx) e [poetry](https://python-poetry.org/docs/).