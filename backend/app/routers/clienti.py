"""
Router per gestione clienti.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cliente
from ..schemas import ClienteCreate, ClienteResponse
from .auth import get_current_user

router = APIRouter(prefix="/clienti", tags=["clienti"])


@router.get("", response_model=list[ClienteResponse])
def list_clienti(db: Session = Depends(get_db), _user=Depends(get_current_user)) -> list[ClienteResponse]:
    return db.query(Cliente).order_by(Cliente.created_at.desc()).all()


@router.post("", response_model=ClienteResponse, status_code=201)
def create_cliente(payload: ClienteCreate, db: Session = Depends(get_db), _user=Depends(get_current_user)) -> ClienteResponse:
    cliente = Cliente(nome=payload.nome, email=payload.email)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: str, db: Session = Depends(get_db), _user=Depends(get_current_user)) -> ClienteResponse:
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente non trovato")
    return cliente
