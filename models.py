from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base, engine
from .schemas import TicketPriority, TicketStatus, UserGroup

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    group = Column(SQLEnum(UserGroup), nullable=False)

    tickets = relationship("Ticket", back_populates="creator")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM)
    group = Column(SQLEnum(UserGroup), nullable=False)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="tickets")


Base.metadata.create_all(bind=engine)