from pydantic import BaseModel
from typing import Optional

# Usuários:

class UsuarioCreate(BaseModel):
  nome: str
  email: str
  senha: str


class UsuarioResponse(BaseModel):
  id: int
  nome: str
  email: str

  class Config:
    orm_mode = True


# Tarefa:

class TarefaCreate(BaseModel):
  titulo: str
  descricao: Optional[str]
  usuario_id: int
  concluida: bool = False


class TarefaResponse(BaseModel):
  id: int
  titulo: str
  descricao: Optional[str]
  usuario_id: int
  concluida: bool

  class Config:
    orm_mode = True