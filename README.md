# AvaliaUNB

# Como rodar o projeto

Instalação de dependências:
- Instalar [docker](https://docs.docker.com/get-docker/)
- Instalar [python](https://www.python.org/downloads/)

Instanciar banco de dados:
- Usando o comando do docker compose: `docker compose up`
- Antes de iniciar a aplicação executar o arquivo `seed.py`
  - Como executar a partir da raíz do projeto: `python3 ./src/seed.py`

Com tudo instalado podemos rodar o projeto:
- Rodar comando `pip install -r requirements.txt` para instalar as dependências
- Rodar o projeto com o comando `flask --app src run --debug`

