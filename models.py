from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, index=True)
  email = Column(String, unique=True)
  senha = Column(String)


class Tarefa(Base):
  __tablename__ = "tarefas"

  id = Column(Integer, primary_key=True, index=True)
  titulo = Column(String, index=True)
  descricao = Column(String, nullable=True)
  usuario_id = Column(Integer, ForeignKey("usuarios.id"))
  concluida = Column(Boolean, default=False)