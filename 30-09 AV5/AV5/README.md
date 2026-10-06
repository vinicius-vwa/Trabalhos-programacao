# AV5 - Sistema de Celulares

Sistema desenvolvido em Python utilizando SQLAlchemy ORM.

O programa permite cadastrar marcas e modelos de celulares através de um relacionamento 1 para N, onde uma marca pode possuir vários modelos.

## Funcionalidades

- Inserir marca
- Inserir modelo
- Listar marcas e modelos
- Excluir marca
- Excluir modelo
- Alterar conexão entre SQLite e MySQL

## Como executar

Entre na pasta do projeto:

cd AV5

Instale as dependências:

uv sync

Execute o programa:

uv run main.py

## Banco de Dados

Ao iniciar o programa, o usuário poderá escolher entre:

1. SQLite
2. MySQL

Os dados de conexão do MySQL são carregados pelo arquivo `.env`.