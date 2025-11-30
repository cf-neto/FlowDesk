from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..core.security import hash_password

router_users = APIRouter(
    prefix="/users",
    tags=["users"]
)

# GET ALL
@router_users.get("/", response_model=list[schemas.UserResponse])
async def get_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# GET BY ID
@router_users.get("/id/{user_id}", response_model=schemas.UserResponse)
async def get_tickets_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O usuário com id {user_id} não foi encontrado"
        )
    
    return user
    

# GET BY EMAIL
@router_users.get("/email/{user_email}", response_model=schemas.UserResponse)
async def get_by_id(user_email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com e-mail {user_email} não encontrado"
        )
    
    return user

# POST CREATE
@router_users.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create(user_in: schemas.User, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    hashed_password = hash_password(user_in.password)

    user = models.User(
        name=user_in.name,
        email=user_in.email,
        group=user_in.group,
        password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# PUT BY ID
@router_users.put("/id/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com id {user_id} não encontrado")

    update_data = user_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

@router_users.delete("/id/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com id {user_id} não encontrado")
    
    db.delete(user)
    db.commit()
