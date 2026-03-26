# Integrador Napp + Único Contato

Este projeto implementa uma API de integração responsável por receber dados de produtos e pedidos do parceiro Napp, armazenar essas informações de forma estruturada e disponibilizá-las para consumo pelo sistema Único Contato.

A aplicação foi construída utilizando Flask, PostgreSQL e SQLAlchemy, com controle de versionamento de banco via Alembic e execução em ambiente containerizado com Docker.


## Objetivo

Centralizar e padronizar a comunicação entre sistemas parceiros, garantindo:

- Recebimento de dados via API (produtos, pedidos, atributos)
- Persistência em banco relacional
- Consulta estruturada para consumo interno
- Atualização de status de pedidos
- Possibilidade de envio de webhooks


## Arquitetura

- API REST em Flask
- Banco de dados PostgreSQL
- ORM com SQLAlchemy
- Migrations com Alembic
- Containerização com Docker


## Estrutura do Projeto


integrador-api/
│
├── app/
│ ├── init.py
│ ├── config.py
│ ├── extensions.py
│ │
│ ├── models/
│ ├── routes/
│
├── migrations/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── .env



## Execução do Projeto

### Subir ambiente com Docker

```bash
docker-compose up -d --build
Verificar containers
docker ps
Testar API
curl http://localhost:5000/health
Banco de Dados

O banco é inicializado via migrations utilizando Alembic.

Caso necessário rodar manualmente:

docker exec -it integrador-api-api-1 bash
alembic upgrade head
DER (Diagrama Entidade-Relacionamento)

Inserir aqui o diagrama do banco

Entidades principais
Seller
Produto
Order
OrderStatus
Imagens
Atributos
Valores de Atributos
Produto x Atributos
Configuração

Arquivo .env:

DATABASE_URL=postgresql://postgres:postgres@db:5432/integrador
Observações
O projeto utiliza migrations para controle de versão do banco.
As tabelas são criadas automaticamente ao subir o container (quando configurado com entrypoint).
A estrutura foi pensada para permitir evolução futura para microserviços.