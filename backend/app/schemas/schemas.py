"""
Pydantic Schemas per l'MVP.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr
    ruolo: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


class RichiestaBase(BaseModel):
    titolo: str = Field(..., min_length=1, max_length=255)
    descrizione: Optional[str] = None
    stato: str = "aperta"
    cliente_id: str


class RichiestaCreate(RichiestaBase):
    pass


class RichiestaResponse(RichiestaBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    utente_id: str
    created_at: datetime


class RichiestaDetail(RichiestaResponse):
    cliente: ClienteResponse
    utente: UserResponse
