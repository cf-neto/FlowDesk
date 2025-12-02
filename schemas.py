from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional

# USER
class UserGroup(str, Enum):
    SERVICE_DESK = "service_desk"
    SISTEMAS = "sistemas"
    DESENVOLVIMENTO = "desenvolvimento"
    INFRAESTRUTURA = "infraestrutura"
    SEGURANCA = "seguranca"
    BANCO_DADOS = "banco_dados"
    GERENCIA_TI = "gerencia_ti"
    RH = "rh"
    FINANCEIRO = "financeiro"
    COMERCIAL = "comercial"
    MARKETING = "marketing"
    OPERACOES = "operacoes"

class User(BaseModel):
    name: str = Field(..., description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    group: UserGroup = Field(..., description="Grupo departamental do usuário")
    password: str = Field(..., min_length=6, description="Senha com mínimo 6 caracteres")

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    group: UserGroup

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    group: Optional[UserGroup] = None
    password: Optional[str] = None

# TICKET
class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TicketBase(BaseModel):
    title: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM
    group: Optional[str]

class TicketCreate(TicketBase):
    created_by: int = Field(..., description="ID do usuário que criou o ticket") # Id do usuário

class TicketResponse(TicketBase):
    id: int
    created_by: int
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime
    updated_at: datetime