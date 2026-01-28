from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

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


@app.get("/usuarios", response_model=List[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos os usuários"""
    usuarios = db.query(models.Usuario).all()
    return usuarios


@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Buscar usuário por ID"""
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario


@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def criar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Criar usuário"""
    db_usuario = models.Usuario(**usuario.dict())
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
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

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
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()

    return {"mensagem": "Usuário deletado com sucesso"}
