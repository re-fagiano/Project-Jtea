"""
Router per gestione richieste.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Cliente, Richiesta, Utente
from ..schemas import RichiestaCreate, RichiestaDetail, RichiestaResponse
from .auth import get_current_user

router = APIRouter(prefix="/richieste", tags=["richieste"])


@router.get("", response_model=list[RichiestaResponse])
def list_richieste(db: Session = Depends(get_db), current_user: Utente = Depends(get_current_user)) -> list[RichiestaResponse]:
    return (
        db.query(Richiesta)
        .filter(Richiesta.utente_id == current_user.id)
        .order_by(Richiesta.created_at.desc())
        .all()
    )


@router.post("", response_model=RichiestaResponse, status_code=status.HTTP_201_CREATED)
def create_richiesta(
    payload: RichiestaCreate,
    db: Session = Depends(get_db),
    current_user: Utente = Depends(get_current_user),
) -> RichiestaResponse:
    cliente = db.query(Cliente).filter(Cliente.id == payload.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente non valido")
    richiesta = Richiesta(
        titolo=payload.titolo,
        descrizione=payload.descrizione,
        stato=payload.stato,
        cliente_id=payload.cliente_id,
        utente_id=current_user.id,
    )
    db.add(richiesta)
    db.commit()
    db.refresh(richiesta)
    return richiesta


@router.get("/{richiesta_id}", response_model=RichiestaDetail)
def get_richiesta(
    richiesta_id: str,
    db: Session = Depends(get_db),
    current_user: Utente = Depends(get_current_user),
) -> RichiestaDetail:
    richiesta = (
        db.query(Richiesta)
        .filter(Richiesta.id == richiesta_id, Richiesta.utente_id == current_user.id)
        .first()
    )
    if not richiesta:
        raise HTTPException(status_code=404, detail="Richiesta non trovata")
    return richiesta
