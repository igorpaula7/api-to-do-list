from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from auth import hash_senha, verificar_senha

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Usuários:


@app.get("/usuarios", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos os usuários"""
    usuarios = db.query(models.Usuario).all()
    return usuarios


@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Buscar usuário por ID"""
    usuario = db.query(models.Usuario).get(usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Criar usuário"""

    senha_hash = hash_senha(usuario.senha)

    db_usuario = models.Usuario(
        nome=usuario.nome, email=usuario.email, senha=senha_hash
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    usuario_atualizado: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
):
    """Atualizar usuário"""
    usuario = db.query(models.Usuario).get(usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email
    usuario.senha = usuario_atualizado.senha

    db.commit()
    db.refresh(usuario)

    return usuario


@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Deletar usuário"""
    usuario = db.query(models.Usuario).get(usuario_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()

    return {"mensagem": "Usuário deletado com sucesso"}


# Tarefas:


@app.get("/tarefas", response_model=List[schemas.TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    """Lista todos as tarefas"""
    tarefas = db.query(models.Tarefa).all()
    return tarefas


@app.get("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def buscar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    """Buscar tarefa por ID"""
    tarefa = db.query(models.Tarefa).get(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return tarefa


@app.post("/tarefas", response_model=schemas.TarefaResponse)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db)):
    """Criar tarefa"""
    db_tarefa = models.Tarefa(**tarefa.dict())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)

    return db_tarefa


@app.put("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def atualizar_tarefa(
    tarefa_id: int,
    tarefa_atualizada: schemas.TarefaCreate,
    db: Session = Depends(get_db),
):
    """Atualizar tarefa"""
    tarefa = db.query(models.Tarefa).get(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa.titulo = tarefa_atualizada.titulo
    tarefa.descricao = tarefa_atualizada.descricao
    tarefa.usuario_id = tarefa_atualizada.usuario_id
    tarefa.concluida = tarefa_atualizada.concluida

    db.commit()
    db.refresh(tarefa)

    return tarefa


@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    """Deletar tarefa"""
    tarefa = db.query(models.Tarefa).get(tarefa_id)

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()

    return {"mensagem": "Tarefa deletada com sucesso"}


@app.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).get(email)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if not verificar_senha(senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta.")

    return {"mensagem": "Login Realizado com Sucesso.", "usuario_id": usuario.id}
