from datetime import timedelta
import uvicorn
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
from starlette.responses import RedirectResponse
app = FastAPI()

# todo - needf to replace this with alembic migrations, eg here https://fastapi.tiangolo.com/tutorial/sql-databases/
models.Base.metadata.create_all(bind=engine)

# todo allow_origins=[*] is not recommended for Production purposes. It is recommended to have specified list of origins
# eg allow_origins=['client-facing-example-app.com', 'localhost:5000']
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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
FastAPI can be run on multiple worker process with the help of Gunicorn server with the help of uvicorn.workers.UvicornWorker worker class. Every worker process starts its instance of FastAPI application on its own Process Id. In order to ensure every instance of application communicates to the database, we will connect and disconnect to the database instance in the FastAPI events  startup and shutdown respectively.
"""

@app.on_event("startup")
async def startup(db: Session = Depends(get_db)):
    await db.connect()

@app.on_event("shutdown")
async def shutdown(db: Session = Depends(get_db)):
    await db.disconnect()


# todo refactor these routes away
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    # todo add password validation
    create_user(db, user)
    return status.HTTP_200_OK

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
