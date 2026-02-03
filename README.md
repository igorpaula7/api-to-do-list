# API To Do List

![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)

## Escopo da solução:

Desenvolvimento de API para sistema de ToDoList, com usuários e tarefas.

## Tecnologias Utilizadas

- FastAPI
- Uvicorn
- SQLAlchemy

## Modelagem de dados

```mermaid
classDiagram
  class Usuario {
    +int id
    +string nome
    +string e-mail
    +string senha
  }

  class Tarefa {
    +int id
    +string titulo
    +string descricao
    +int usuario_id
    +bool concluida
  }

  Usuario "1" --> "*" Tarefa : possui
```

## Endpoints:

### Usuários:

`GET /usuarios` - Lista todos os usuários;  
`GET /usuarios{id}` - Busca usuário por ID;  
`POST /usuarios` - Cria novo usuário;  
`PUT /usuarios/{id}` - Altera um usuário existente;  
`DELETE /usuarios/{id}` - Deleta um usuário.  
`POST /login` - Efetua o login na aplicação.

### Tarefas:

`GET /tarefas` - Lista todas as tarefas;  
`GET /tarefas/{id}` - Busca uma tarefa específica;  
`POST /tarefas` - Adiciona uma tarefa;  
`PUT /tarefas/{id}` - Altera uma tarefa;  
`DELETE /tarefas/{id}` - Deleta uma tarefa.
