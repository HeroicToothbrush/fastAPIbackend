from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from . import models
from .auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_user, create_access_token, \
    get_current_active_user
from .database import engine
from .database import get_db
from .schemas import Token, User, UserCreate

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

db = get_db()


@app.get("/")
async def home():
    return {"message": "This is the homepage"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/create/")
async def create_new_user(user: UserCreate):
    # todo add password validation
    create_user(db, user)
    return status.HTTP_200_OK
