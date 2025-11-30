from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..core.security import hash_password
from datetime import datetime

router_tickets = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)


@router_tickets.get("/", response_model=list[schemas.TicketResponse])
async def get_all(db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).all()
    return tickets

@router_tickets.get("/id/{ticket_id}", response_model=schemas.TicketResponse)
async def get_by_id(ticket_id: int, db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not tickets:  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Ticket com id {ticket_id} não encontrado"
        )
    
    return tickets

@router_tickets.get("/users/{user_id}", response_model=list[schemas.TicketResponse])
async def get_tickets_by_user(user_id: int, db: Session = Depends(get_db)):
    # Verificar se o usuário existe
    user_exists = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {user_id} não encontrado"
        )
    
    user_tickets = db.query(models.Ticket).filter(models.Ticket.created_by == user_id).all()
    return user_tickets


@router_tickets.post("/", response_model=schemas.TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_in: schemas.TicketCreate, db: Session = Depends(get_db)):
    
    # Verificar se o usuário criador existe
    user_exists = db.query(models.User).filter(models.User.id == ticket_in.created_by).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com id {ticket_in.created_by} não encontrado"
        )
    
    now = datetime.now()
    new_ticket = models.Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        priority=ticket_in.priority,
        group=ticket_in.group,
        created_by=ticket_in.created_by,
        status=schemas.TicketStatus.OPEN, 
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

@router_tickets.delete("/id/{ticket_id}", response_model=schemas.TicketResponse)
async def delete(ticket_id: int, db: Session = Depends(get_db)):
    # Verificar se o usuário criador existe
    user_exists = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket com id {ticket_id} não encontrado"
        )
    
    db.delete(ticket_id)
    db.commit()
    return {"message": "Ticket deletado com sucesso"}