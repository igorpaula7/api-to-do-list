from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, SessionLocal

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