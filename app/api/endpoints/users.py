from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.auth import create_user, get_current_active_user
from app.database import get_db
from app.schemas import User, UserCreate

router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/users/create/")
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    # todo add password validation
    create_user(db, user)
    return status.HTTP_200_OK
