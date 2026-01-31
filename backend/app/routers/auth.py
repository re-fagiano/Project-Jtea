"""
Router per autenticazione e utenti.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import Utente
from ..schemas import Token, UserCreate, UserResponse
from ..utils import create_access_token, get_password_hash, verify_password

settings = get_settings()

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_user_by_email(db: Session, email: str) -> Utente | None:
    return db.query(Utente).filter(Utente.email == email).first()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Utente:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenziali non valide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str | None = payload.get("sub")
    except JWTError as exc:
        raise credentials_exception from exc
    if not user_id:
        raise credentials_exception
    user = db.query(Utente).filter(Utente.id == user_id).first()
    if not user:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email già registrata")
    user = Utente(
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        ruolo=payload.ruolo,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenziali non valide")
    access_token = create_access_token(subject=user.id, ruolo=user.ruolo.value)
    return Token(access_token=access_token)


@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: Utente = Depends(get_current_user)) -> UserResponse:
    return current_user
