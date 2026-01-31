"""
Modelli SQLAlchemy principali per l'MVP.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from ..database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    supervisore = "supervisore"
    tecnico = "tecnico"
    cliente = "cliente"


class Utente(Base):
    __tablename__ = "utenti"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    ruolo = Column(SQLEnum(UserRole), nullable=False, default=UserRole.cliente)
    created_at = Column(DateTime, default=datetime.utcnow)

    richieste = relationship("Richiesta", back_populates="utente", cascade="all, delete-orphan")


class Cliente(Base):
    __tablename__ = "clienti"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    richieste = relationship("Richiesta", back_populates="cliente", cascade="all, delete-orphan")


class Richiesta(Base):
    __tablename__ = "richieste"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titolo = Column(String(255), nullable=False)
    descrizione = Column(Text)
    stato = Column(String(50), nullable=False, default="aperta")
    cliente_id = Column(String(36), ForeignKey("clienti.id"), nullable=False)
    utente_id = Column(String(36), ForeignKey("utenti.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="richieste")
    utente = relationship("Utente", back_populates="richieste")
