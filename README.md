# API Restful de Blog com FastAPI e SQLAlchemy Core

API RESTful completa para gerenciamento de usuários, autenticação via tokens JWT e publicação de postagens, construída com **FastAPI**, **Databases (Async)**, **SQLAlchemy Core** e testada de forma assíncrona com **Pytest** e **HTTPX**.


## 🛠️ Tecnologias e Ferramentas

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Banco de Dados & ORM/Core:** SQLite / PostgreSQL, SQLAlchemy Core, `databases` (execução assíncrona de queries)
- **Validação de Dados:** Pydantic v2
- **Segurança & Autenticação:** PyJWT, Passlib / OAuth2 Bearer Token
- **Testes de Integração:** Pytest, Pytest-Asyncio, HTTPX


## 📂 Estrutura do Projeto

A arquitetura segue uma divisão clara de responsabilidades no padrão MVC/Clean Architecture adaptado para APIs:

```text
fastAPI/
├── src/
│   ├── controllers/      # Roteadores/Endpoints do FastAPI (auth, post, user)
│   ├── models/           # Definição das tabelas do banco de dados (SQLAlchemy Core)
│   ├── schemas/          # Schemas Pydantic para validação de entrada (In/Update)
│   ├── views/            # Schemas Pydantic para formatação de saída/DTOs (Out)
│   ├── services/         # Regras de negócio e acesso ao banco de dados
│   ├── database.py       # Conexão assíncrona com o banco e metadados
│   ├── main.py           # Ponto de entrada da aplicação FastAPI
│   └── security.py       # Funções de autenticação e manipulação de tokens JWT
├── tests/                # Testes de integração assíncronos com Pytest
│   ├── conftest.py       # Fixtures globais do banco e cliente de teste HTTPX
│   └── integration/      # Casos de testes das APIs
├── blog.sqlite           # Banco de dados local (desenvolvimento)
├── .gitignore
└── README.md
```

## 🚀 Como Executar o Projeto
### Pró-requisitos
* Python 3.10 ou superior
* Git instalado

### 1. Clonar o repositório e acessar a pasta
```
Bash

git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd fastAPI
```

### 2. Criar e ativar o ambiente virtual
```
Bash

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências
```
Bash

pip install fastapi uvicorn databases[sqlite] sqlalchemy pydantic passlib[bcrypt] pyjwt pytest pytest-asyncio httpx
```

### 4. Executar a aplicação
```
Bash

uvicorn src.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`

## 📑 Documentação Interativa (Swagger / Redoc)
Com o servidor rodando, acesse a documentação gerada automaticamente pelo FastAPI:
* __Swagger UI__: `http://127.0.0.1:8000/docs`
* __ReDoc__: `http://127.0.0.1:8000/redoc`

## 🧪 Executando os Testes
Os testes são executados em um banco de dados SQLite isolado (`tests.db`).
Para rodar toda a suíte de testes de integração:

```
Bash

pytest
```

para ver a saída detalhada dos testes:
```
Bash

pteste -v
```

## 📌 Principais Endpoints
### 🔐 Autenticação (`/auth`)
* `POST /auth/login` - Autentica o usuário e retorna o token de acesso Bearer JWT.

### 👤 Usuários (`/users`)
* `POST /users/` - Cadastra um novo usuário.

* `GET /users/` - Lista usuários com paginação (`limit`, `skip`).

* `GET /users/{id}` - Obtém detalhes de um usuário específico.

* `PATCH /users/{id}` - Atualiza parcialmente dados de um usuário.

* `DELETE /users/{id}` - Remove um usuário.

### 📝 Postagens (`/posts`) (Requer Autenticação)
* `POST /posts/` - Cria um novo post.

* `GET /posts/` - Lista posts filtrando por status (`published=on/off`) e paginação.

* `GET /posts/{id}` - Obtém um post pelo ID.

* `PATCH /posts/{id}` - Atualiza dados de um post.

* `DELETE /posts/{id}` - Remove um post pelo ID.